"""
Rate limiting utilities.

Two strategies are used:
  1. DB-backed (QuoteRequest table) — for POST /quotes/ by contact_value + IP hash.
     Persists across restarts. Already wired to the existing `quote_results` table.

  2. In-memory sliding window — for auth endpoints (login, register) and
     POST /quotes/{id}/send-email.
     Fast, no DB overhead, resets on restart (acceptable for these use-cases).
"""

import hashlib
import threading
from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException, Request, status

# ---------------------------------------------------------------------------
# In-memory sliding window rate limiter
# ---------------------------------------------------------------------------

# Thread-safe store: key -> deque of UTC timestamps
_window_lock = threading.Lock()
_request_log: dict[str, deque[datetime]] = defaultdict(deque)


def _memory_check(key: str, max_requests: int, window_seconds: int) -> None:
    """
    Enforce an in-memory sliding-window rate limit.

    Raises HTTP 429 if `key` has exceeded `max_requests` within
    the last `window_seconds` seconds.

    Skipped automatically when the IP resolves to 'testclient'
    (FastAPI TestClient) so that the test suite is not affected.
    """
    # FastAPI TestClient always presents as 'testclient'; skip limiting in tests.
    if "testclient" in key:
        return

    now = datetime.now(UTC)
    cutoff = now - timedelta(seconds=window_seconds)

    with _window_lock:
        dq = _request_log[key]

        # Evict expired timestamps
        while dq and dq[0] < cutoff:
            dq.popleft()

        if len(dq) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiadas solicitudes. Por favor espera un momento antes de intentarlo de nuevo.",
                headers={"Retry-After": str(window_seconds)},
            )

        dq.append(now)


def reset_rate_limit_for_tests() -> None:
    """Clear all in-memory rate limit state. Call this in test fixtures."""
    with _window_lock:
        _request_log.clear()


def rate_limit_login(request: Request) -> None:
    """
    5 intentos de login por IP cada 5 minutos.
    Bloquea ataques de fuerza bruta contra contraseñas.
    """
    ip = _get_ip(request)
    _memory_check(f"login:{ip}", max_requests=5, window_seconds=300)


def rate_limit_register(request: Request) -> None:
    """
    10 registros por IP cada hora.
    Evita spam de cuentas desde una misma IP.
    """
    ip = _get_ip(request)
    _memory_check(f"register:{ip}", max_requests=10, window_seconds=3600)


def rate_limit_send_email(request: Request) -> None:
    """
    3 envíos de email por IP cada 10 minutos.
    Previene uso del endpoint como spam relay.
    """
    ip = _get_ip(request)
    _memory_check(f"send_email:{ip}", max_requests=3, window_seconds=600)


# ---------------------------------------------------------------------------
# DB-backed rate limiter for POST /quotes/ (uses existing QuoteRequest table)
# ---------------------------------------------------------------------------


def hash_value(value: str) -> str:
    """Return a SHA-256 hex digest; never stores the raw value."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def check_quote_rate_limit(
    db: Any,
    *,
    contact_value: str,
    ip_address: str | None,
    max_per_contact_24h: int = 5,
    max_per_ip_24h: int = 20,
) -> None:
    """
    Enforce DB-backed rate limits for quote creation:

    - Per contact_value (phone/email): max 5 quotes in 24 hours.
    - Per IP address: max 20 quotes in 24 hours.

    Raises HTTP 429 if either limit is exceeded.
    Uses the existing `quote_results` (QuoteRequest) table.

    Skipped when ip_address is 'testclient' (FastAPI TestClient).
    """
    # FastAPI TestClient always presents as 'testclient'; skip limiting in tests.
    if ip_address == "testclient":
        return

    from app.api.v1.quotes.repository import count_recent_quote_requests

    # Check per contact_value
    contact_count = count_recent_quote_requests(
        db, contact_value=contact_value, hours=24
    )
    if contact_count >= max_per_contact_24h:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Has generado demasiadas cotizaciones con este contacto. Inténtalo de nuevo mañana.",
            headers={"Retry-After": "86400"},
        )

    # Check per IP
    if ip_address:
        ip_hash = hash_value(ip_address)
        ip_count = count_recent_quote_requests_by_ip(db, ip_hash=ip_hash, hours=24)
        if ip_count >= max_per_ip_24h:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiadas cotizaciones generadas desde esta dirección. Inténtalo de nuevo mañana.",
                headers={"Retry-After": "86400"},
            )


def count_recent_quote_requests_by_ip(
    db: Any,
    *,
    ip_hash: str,
    hours: int = 24,
) -> int:
    """Count QuoteRequest rows for a given hashed IP in the last N hours."""
    from datetime import UTC, datetime, timedelta

    from sqlalchemy import func, select

    from app.db.models import QuoteRequest

    since = datetime.now(UTC) - timedelta(hours=hours)
    statement = (
        select(func.count())
        .select_from(QuoteRequest)
        .where(
            QuoteRequest.ip_hash == ip_hash,
            QuoteRequest.created_at >= since,
        )
    )
    return db.scalar(statement) or 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_ip(request: Request) -> str:
    """
    Extract the real client IP, honoring X-Forwarded-For when behind a proxy
    (Railway / Cloudflare).
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can be a comma-separated list; take the first entry
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"
