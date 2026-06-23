"""
Tests para Evento de Rifa:

    Todos los tests corren usando la base de datos aislada de sqlite.

    Para poder simular el test se re-creo un evento "rifa":
        - se inventaron los códigos.
        - se simularon los registros de usuario y elección de números.

    Cada test recibe un nuevo `client` (desde conftest.py) mas un nuevo evento de "rifa" (raffle).
"""

import hashlib

import pytest
from fastapi.testclient import TestClient

from app.api.v1.raffle.models import (
    Raffle,
    RaffleBranch,
    RaffleNumber,
    RaffleTicketCode,
)
from tests.helpers import register_payload

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hash(code: str) -> str:
    return hashlib.sha256(code.strip().upper().encode()).hexdigest()


def _make_headers(client: TestClient) -> dict[str, str]:
    """Register a fresh user and return Authorization headers."""
    payload = register_payload()
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Raffle fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def raffle_env(client: TestClient):
    """
    Construye un evento nuevo de Rifa en SQLite

    Hace un return del diccionario como:
        raffle          - the Raffle ORM object
        branch          - the first (and only) RaffleBranch
        available_code  - a RaffleTicketCode with status='available'
        used_code       - a RaffleTicketCode with status='used'
        number_1        - RaffleNumber #1 (available)
        number_2        - RaffleNumber #2 (available)
    """
    # Access the overridden DB via the app dependency
    from app.db.session import get_db
    from app.main import app

    db = next(app.dependency_overrides[get_db]())

    raffle = Raffle(
        title="Sorteo Test",
        slug="sorteo-test-2099",
        prize_title="Premio de prueba",
        status="active",
        total_numbers=10,
        numbers_per_branch=10,
        max_codes_per_batch=5,
        max_batches_per_user_24h=3,
    )
    db.add(raffle)
    db.flush()

    branch = RaffleBranch(
        raffle_id=raffle.id,
        name="Sucursal Test",
        slug="sucursal-test",
        image_url=None,
        number_start=1,
        number_end=10,
        sort_order=1,
        status="active",
    )
    db.add(branch)
    db.flush()

    # Add 10 numbers for this branch
    numbers = []
    for n in range(1, 11):
        rn = RaffleNumber(
            raffle_id=raffle.id,
            branch_id=branch.id,
            number=n,
            status="available",
        )
        db.add(rn)
        numbers.append(rn)
    db.flush()

    # One available ticket code
    available_code = RaffleTicketCode(
        raffle_id=raffle.id,
        code_hash=_hash("TEST-AVAIL-0001"),
        code_last4="0001",
        status="available",
    )
    db.add(available_code)

    # A second code (also available) for multi-code tests
    available_code_2 = RaffleTicketCode(
        raffle_id=raffle.id,
        code_hash=_hash("TEST-AVAIL-0002"),
        code_last4="0002",
        status="available",
    )
    db.add(available_code_2)

    # One already-used ticket code
    used_code = RaffleTicketCode(
        raffle_id=raffle.id,
        code_hash=_hash("TEST-USED-9999"),
        code_last4="9999",
        status="used",
    )
    db.add(used_code)

    db.commit()

    for obj in [raffle, branch, available_code, available_code_2, used_code] + numbers:
        db.refresh(obj)

    return {
        "raffle": raffle,
        "branch": branch,
        "available_code": available_code,
        "available_code_2": available_code_2,
        "used_code": used_code,
        "numbers": numbers,
        "number_1": numbers[0],
        "number_2": numbers[1],
    }


# ---------------------------------------------------------------------------
# Auth wall: every raffle endpoint requires a logged-in user
# ---------------------------------------------------------------------------


class TestRaffleAuthRequired:
    def test_status_requires_auth(self, client: TestClient):
        resp = client.get("/api/v1/raffle/status")
        assert (
            resp.status_code == 401
        )  # HTTPBearer returns 401 when no Authorization header

    def test_branch_numbers_requires_auth(self, client: TestClient):
        resp = client.get("/api/v1/raffle/branches/1/numbers")
        assert resp.status_code == 401

    def test_validate_tickets_requires_auth(self, client: TestClient):
        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": 1, "codes": ["ABC"]},
        )
        assert resp.status_code == 401

    def test_confirm_numbers_requires_auth(self, client: TestClient):
        resp = client.post(
            "/api/v1/raffle/numbers/confirm",
            json={"batch_id": 1, "selections": []},
        )
        assert resp.status_code == 401

    def test_my_entries_requires_auth(self, client: TestClient):
        resp = client.get("/api/v1/raffle/me/entries")
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# No active raffle
# ---------------------------------------------------------------------------


class TestNoActiveRaffle:
    """Tests that run against a DB with no raffle seeded."""

    def test_status_returns_404_when_no_active_raffle(self, client: TestClient):
        headers = _make_headers(client)
        resp = client.get("/api/v1/raffle/status", headers=headers)
        assert resp.status_code == 404

    def test_validate_tickets_returns_404_when_no_active_raffle(
        self, client: TestClient
    ):
        headers = _make_headers(client)
        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": 1, "codes": ["SOME-CODE"]},
            headers=headers,
        )
        assert resp.status_code == 404

    def test_my_entries_returns_404_when_no_active_raffle(self, client: TestClient):
        headers = _make_headers(client)
        resp = client.get("/api/v1/raffle/me/entries", headers=headers)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /raffle/status
# ---------------------------------------------------------------------------


class TestRaffleStatus:
    def test_returns_raffle_info(self, client: TestClient, raffle_env: dict):
        headers = _make_headers(client)
        resp = client.get("/api/v1/raffle/status", headers=headers)

        assert resp.status_code == 200
        data = resp.json()

        assert data["title"] == "Sorteo Test"
        assert data["prize_title"] == "Premio de prueba"
        assert data["status"] == "active"
        assert data["total_numbers"] == 10

    def test_includes_active_branches(self, client: TestClient, raffle_env: dict):
        headers = _make_headers(client)
        resp = client.get("/api/v1/raffle/status", headers=headers)

        assert resp.status_code == 200
        branches = resp.json()["branches"]

        assert len(branches) == 1
        assert branches[0]["name"] == "Sucursal Test"
        assert branches[0]["slug"] == "sucursal-test"
        assert branches[0]["number_start"] == 1
        assert branches[0]["number_end"] == 10


# ---------------------------------------------------------------------------
# GET /raffle/branches/{id}/numbers
# ---------------------------------------------------------------------------


class TestBranchNumbers:
    def test_returns_numbers_for_valid_branch(
        self, client: TestClient, raffle_env: dict
    ):
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.get(
            f"/api/v1/raffle/branches/{branch_id}/numbers", headers=headers
        )

        assert resp.status_code == 200
        numbers = resp.json()
        assert len(numbers) == 10
        assert numbers[0]["number"] == 1
        assert numbers[0]["status"] == "available"

    def test_returns_empty_list_for_nonexistent_branch(
        self, client: TestClient, raffle_env: dict
    ):
        """
        GET /branches/{id}/numbers with a branch_id not in the active raffle
        returns 200 with an empty list — the route calls get_numbers_by_branch
        directly (no prior get_branch_by_id guard), which simply returns []
        when no RaffleNumber rows match raffle_id + branch_id.
        """
        headers = _make_headers(client)
        resp = client.get("/api/v1/raffle/branches/99999/numbers", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == []


# ---------------------------------------------------------------------------
# POST /raffle/tickets/validate
# ---------------------------------------------------------------------------


class TestValidateTickets:
    def test_accepts_valid_available_code(self, client: TestClient, raffle_env: dict):
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["TEST-AVAIL-0001"]},
            headers=headers,
        )

        assert resp.status_code == 200
        data = resp.json()
        assert data["submitted_count"] == 1
        assert data["accepted_count"] == 1
        assert data["rejected_count"] == 0
        assert data["results"][0]["status"] == "accepted"
        assert data["results"][0]["reason"] is None

    def test_rejects_unknown_code(self, client: TestClient, raffle_env: dict):
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["CODIGO-QUE-NO-EXISTE"]},
            headers=headers,
        )

        assert resp.status_code == 200
        data = resp.json()
        assert data["accepted_count"] == 0
        assert data["rejected_count"] == 1
        assert data["results"][0]["status"] == "rejected"
        assert data["results"][0]["reason"] == "not_found"

    def test_rejects_already_used_code(self, client: TestClient, raffle_env: dict):
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["TEST-USED-9999"]},
            headers=headers,
        )

        assert resp.status_code == 200
        data = resp.json()
        assert data["rejected_count"] == 1
        assert data["results"][0]["status"] == "rejected"
        assert data["results"][0]["reason"] == "already_used"

    def test_rejects_duplicate_in_same_batch(
        self, client: TestClient, raffle_env: dict
    ):
        """Sending the same code twice in one batch → one accepted, one duplicate_in_batch."""
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={
                "branch_id": branch_id,
                "codes": ["TEST-AVAIL-0001", "TEST-AVAIL-0001"],
            },
            headers=headers,
        )

        assert resp.status_code == 200
        data = resp.json()
        assert data["submitted_count"] == 2
        assert data["accepted_count"] == 1
        assert data["rejected_count"] == 1

        reasons = {r["reason"] for r in data["results"]}
        assert "duplicate_in_batch" in reasons

    def test_code_validation_is_case_insensitive(
        self, client: TestClient, raffle_env: dict
    ):
        """'test-avail-0001' must match 'TEST-AVAIL-0001' after normalization."""
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["test-avail-0001"]},
            headers=headers,
        )

        assert resp.status_code == 200
        assert resp.json()["accepted_count"] == 1

    def test_rejects_batch_exceeding_max_codes(
        self, client: TestClient, raffle_env: dict
    ):
        """max_codes_per_batch=5; sending 6 codes → 400."""
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={
                "branch_id": branch_id,
                "codes": ["A", "B", "C", "D", "E", "F"],  # 6 > max of 5
            },
            headers=headers,
        )

        assert resp.status_code == 400
        assert "boletos" in resp.json()["detail"].lower()

    def test_rejects_empty_codes_list(self, client: TestClient, raffle_env: dict):
        """Schema requires at least 1 code → 422."""
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": []},
            headers=headers,
        )

        assert resp.status_code == 422

    def test_respects_max_batches_per_user_24h(
        self, client: TestClient, raffle_env: dict
    ):
        """
        max_batches_per_user_24h=3. After 3 successful batches the 4th must
        return 429. Uses a single user across all 3 batches.
        """
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        for _ in range(3):
            resp = client.post(
                "/api/v1/raffle/tickets/validate",
                json={"branch_id": branch_id, "codes": ["CODIGO-INEXISTENTE"]},
                headers=headers,
            )
            assert resp.status_code == 200

        # 4th attempt should be throttled
        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["OTRO-CODIGO"]},
            headers=headers,
        )
        assert resp.status_code == 429

    def test_returns_last4_digits_of_code(self, client: TestClient, raffle_env: dict):
        """code_last4 must be the last 4 chars of the normalized code."""
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["TEST-AVAIL-0001"]},
            headers=headers,
        )

        assert resp.status_code == 200
        # Normalized: "TESTAVAIL0001" → last4 = "0001"
        assert resp.json()["results"][0]["code_last4"] == "0001"

    def test_stores_ticket_code_id_for_accepted_codes(
        self, client: TestClient, raffle_env: dict
    ):
        """Accepted results must include the ticket_code_id so confirm can reference them."""
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["TEST-AVAIL-0001"]},
            headers=headers,
        )

        assert resp.status_code == 200
        result = resp.json()["results"][0]
        assert result["status"] == "accepted"
        assert result["ticket_code_id"] is not None
        assert isinstance(result["ticket_code_id"], int)


# ---------------------------------------------------------------------------
# POST /raffle/numbers/confirm
# ---------------------------------------------------------------------------


class TestConfirmNumbers:
    def _validate_and_get_batch(
        self,
        client: TestClient,
        headers: dict,
        branch_id: int,
        code: str,
    ) -> dict:
        """Helper: validate a code and return the full batch response."""
        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": [code]},
            headers=headers,
        )
        assert resp.status_code == 200
        return resp.json()

    def test_confirm_assigns_number_to_user(self, client: TestClient, raffle_env: dict):
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id
        number_1 = raffle_env["number_1"]

        batch = self._validate_and_get_batch(
            client, headers, branch_id, "TEST-AVAIL-0001"
        )

        ticket_code_id = batch["results"][0]["ticket_code_id"]

        resp = client.post(
            "/api/v1/raffle/numbers/confirm",
            json={
                "batch_id": batch["batch_id"],
                "selections": [
                    {
                        "ticket_code_id": ticket_code_id,
                        "raffle_number_id": number_1.id,
                    }
                ],
            },
            headers=headers,
        )

        assert resp.status_code == 200
        entries = resp.json()
        assert len(entries) == 1
        assert entries[0]["selected_number"] == 1
        assert entries[0]["branch_id"] == branch_id

    def test_confirm_marks_code_as_used(self, client: TestClient, raffle_env: dict):
        """After confirming, the same ticket code must be rejected as 'already_used'."""
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id
        number_1 = raffle_env["number_1"]

        # First: validate + confirm
        batch = self._validate_and_get_batch(
            client, headers, branch_id, "TEST-AVAIL-0001"
        )
        ticket_code_id = batch["results"][0]["ticket_code_id"]

        client.post(
            "/api/v1/raffle/numbers/confirm",
            json={
                "batch_id": batch["batch_id"],
                "selections": [
                    {"ticket_code_id": ticket_code_id, "raffle_number_id": number_1.id}
                ],
            },
            headers=headers,
        )

        # Now try to use the same code again via a new batch from another user
        headers_2 = _make_headers(client)
        resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["TEST-AVAIL-0001"]},
            headers=headers_2,
        )
        assert resp.status_code == 200
        assert resp.json()["results"][0]["reason"] == "already_used"

    def test_confirm_marks_number_as_taken(self, client: TestClient, raffle_env: dict):
        """After confirming, the same raffle number must be unavailable for a second user."""
        headers_1 = _make_headers(client)
        headers_2 = _make_headers(client)
        branch_id = raffle_env["branch"].id
        number_1 = raffle_env["number_1"]

        # User 1 confirms number_1 with code 0001
        batch1 = self._validate_and_get_batch(
            client, headers_1, branch_id, "TEST-AVAIL-0001"
        )
        client.post(
            "/api/v1/raffle/numbers/confirm",
            json={
                "batch_id": batch1["batch_id"],
                "selections": [
                    {
                        "ticket_code_id": batch1["results"][0]["ticket_code_id"],
                        "raffle_number_id": number_1.id,
                    }
                ],
            },
            headers=headers_1,
        )

        # User 2 tries to confirm the same number_1 with code 0002
        batch2 = self._validate_and_get_batch(
            client, headers_2, branch_id, "TEST-AVAIL-0002"
        )
        resp = client.post(
            "/api/v1/raffle/numbers/confirm",
            json={
                "batch_id": batch2["batch_id"],
                "selections": [
                    {
                        "ticket_code_id": batch2["results"][0]["ticket_code_id"],
                        "raffle_number_id": number_1.id,
                    }
                ],
            },
            headers=headers_2,
        )
        assert resp.status_code == 409
        assert "número" in resp.json()["detail"].lower()

    def test_confirm_rejects_mismatched_selection_count(
        self, client: TestClient, raffle_env: dict
    ):
        """
        Batch accepted 1 ticket but confirm sends 0 selections →
        must return 400 (count mismatch).
        """
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        batch = self._validate_and_get_batch(
            client, headers, branch_id, "TEST-AVAIL-0001"
        )

        resp = client.post(
            "/api/v1/raffle/numbers/confirm",
            json={
                "batch_id": batch["batch_id"],
                "selections": [],  # 0 selections, but 1 was accepted
            },
            headers=headers,
        )

        assert resp.status_code == 422  # Pydantic: min_length=1 on selections

    def test_confirm_rejects_foreign_batch(self, client: TestClient, raffle_env: dict):
        """
        User B cannot confirm a batch created by User A.
        get_batch_accepted_items filters by user_id, so selections will
        not match → 400 (mismatch or ticket not in batch).
        """
        headers_a = _make_headers(client)
        headers_b = _make_headers(client)
        branch_id = raffle_env["branch"].id
        number_1 = raffle_env["number_1"]

        # User A validates a code
        batch_a = self._validate_and_get_batch(
            client, headers_a, branch_id, "TEST-AVAIL-0001"
        )
        ticket_code_id = batch_a["results"][0]["ticket_code_id"]

        # User B tries to confirm User A's batch
        resp = client.post(
            "/api/v1/raffle/numbers/confirm",
            json={
                "batch_id": batch_a["batch_id"],
                "selections": [
                    {
                        "ticket_code_id": ticket_code_id,
                        "raffle_number_id": number_1.id,
                    }
                ],
            },
            headers=headers_b,
        )

        assert resp.status_code == 400

    def test_confirm_rejects_invalid_raffle_number_id(
        self, client: TestClient, raffle_env: dict
    ):
        """Passing a non-existent raffle_number_id → 404."""
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id

        batch = self._validate_and_get_batch(
            client, headers, branch_id, "TEST-AVAIL-0001"
        )
        ticket_code_id = batch["results"][0]["ticket_code_id"]

        resp = client.post(
            "/api/v1/raffle/numbers/confirm",
            json={
                "batch_id": batch["batch_id"],
                "selections": [
                    {
                        "ticket_code_id": ticket_code_id,
                        "raffle_number_id": 999999,
                    }
                ],
            },
            headers=headers,
        )

        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /raffle/me/entries
# ---------------------------------------------------------------------------


class TestMyEntries:
    def test_returns_empty_list_for_new_user(
        self, client: TestClient, raffle_env: dict
    ):
        headers = _make_headers(client)
        resp = client.get("/api/v1/raffle/me/entries", headers=headers)

        assert resp.status_code == 200
        assert resp.json() == []

    def test_returns_entry_after_confirm(self, client: TestClient, raffle_env: dict):
        headers = _make_headers(client)
        branch_id = raffle_env["branch"].id
        number_1 = raffle_env["number_1"]

        # Validate + confirm
        batch_resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["TEST-AVAIL-0001"]},
            headers=headers,
        )
        batch = batch_resp.json()
        ticket_code_id = batch["results"][0]["ticket_code_id"]

        client.post(
            "/api/v1/raffle/numbers/confirm",
            json={
                "batch_id": batch["batch_id"],
                "selections": [
                    {"ticket_code_id": ticket_code_id, "raffle_number_id": number_1.id}
                ],
            },
            headers=headers,
        )

        # Now check entries
        resp = client.get("/api/v1/raffle/me/entries", headers=headers)
        assert resp.status_code == 200

        entries = resp.json()
        assert len(entries) == 1
        assert entries[0]["selected_number"] == 1

    def test_only_returns_own_entries(self, client: TestClient, raffle_env: dict):
        """User A's entries must not appear in User B's /me/entries."""
        headers_a = _make_headers(client)
        headers_b = _make_headers(client)
        branch_id = raffle_env["branch"].id
        number_1 = raffle_env["number_1"]

        # User A completes a full flow
        batch_resp = client.post(
            "/api/v1/raffle/tickets/validate",
            json={"branch_id": branch_id, "codes": ["TEST-AVAIL-0001"]},
            headers=headers_a,
        )
        batch = batch_resp.json()
        client.post(
            "/api/v1/raffle/numbers/confirm",
            json={
                "batch_id": batch["batch_id"],
                "selections": [
                    {
                        "ticket_code_id": batch["results"][0]["ticket_code_id"],
                        "raffle_number_id": number_1.id,
                    }
                ],
            },
            headers=headers_a,
        )

        # User B should see an empty list
        resp_b = client.get("/api/v1/raffle/me/entries", headers=headers_b)
        assert resp_b.status_code == 200
        assert resp_b.json() == []
