from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Quote, QuoteRequest


def create_quote_record(
    db: Session,
    *,
    customer_name: str,
    contact_method: str,
    contact_value: str,
    state: str,
    city: str,
    postal_code: str,
    square_meters: float,
    paint_product: str,
    estimated_price: float,
    payload_json: dict[str, Any],
    result_json: dict[str, Any],
    user_id: int | None = None,
    user_type: str = "visitor",
    status: str = "created",
) -> Quote:

    quote = Quote(
        customer_name=customer_name,
        contact_method=contact_method,
        contact_value=contact_value,
        state=state,
        city=city,
        postal_code=postal_code,
        square_meters=square_meters,
        paint_product=paint_product,
        estimated_price=estimated_price,
        payload_json=payload_json,
        result_json=result_json,
        user_id=user_id,
        user_type=user_type,
        status=status,
    )

    db.add(quote)
    db.commit()
    db.refresh(quote)

    return quote


def create_quote_request_record(
    db: Session,
    *,
    contact_value: str,
    ip_hash: str | None = None,
    user_agent_hash: str | None = None,
    reason: str = "quote_created",
) -> QuoteRequest:
    quote_request = QuoteRequest(
        contact_value=contact_value,
        ip_hash=ip_hash,
        user_agent_hash=user_agent_hash,
        reason=reason,
    )

    db.add(quote_request)
    db.commit()
    db.refresh(quote_request)

    return quote_request


def count_recent_quote_requests(
    db: Session,
    *,
    contact_value: str,
    hours: int = 24,
) -> int:
    since = datetime.now(UTC) - timedelta(hours=hours)

    statement = (
        select(func.count())
        .select_from(QuoteRequest)
        .where(
            QuoteRequest.contact_value == contact_value,
            QuoteRequest.created_at >= since,
        )
    )

    return db.scalar(statement) or 0


def get_user_quotes(db: Session, user_id: int) -> list[Quote]:
    statement = (
        select(Quote).where(Quote.user_id == user_id).order_by(Quote.created_at.desc())
    )
    return list(db.scalars(statement).all())


def get_quote_by_id(db: Session, quote_id: int) -> Quote | None:
    statement = select(Quote).where(Quote.id == quote_id)
    return db.scalar(statement)


def count_user_quotes(db: Session, user_id: int) -> int:
    statement = select(func.count()).select_from(Quote).where(Quote.user_id == user_id)
    return db.scalar(statement) or 0


def delete_quote_record(db: Session, quote: Quote) -> None:
    db.delete(quote)
    db.commit()
