from fastapi.testclient import TestClient

from tests.helpers import register_payload, unique_email


def test_register_user_returns_token_and_user(client: TestClient):
    payload = register_payload()

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    assert data["user"]["full_name"] == payload["full_name"]
    assert data["user"]["email"] == payload["email"]
    assert data["user"]["phone"] == payload["phone"]
    assert data["user"]["is_active"] is True
    assert data["user"]["is_admin"] is False

    assert "password" not in data["user"]
    assert "password_hash" not in data["user"]


def test_login_user_returns_token(client: TestClient):
    payload = register_payload()

    register_response = client.post("/api/v1/auth/register", json=payload)
    assert register_response.status_code == 200

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == payload["email"]


def test_register_rejects_duplicate_email(client: TestClient):
    email = unique_email()

    first_payload = register_payload(email=email)
    second_payload = register_payload(email=email)

    first_response = client.post("/api/v1/auth/register", json=first_payload)
    assert first_response.status_code == 200

    second_response = client.post("/api/v1/auth/register", json=second_payload)

    assert second_response.status_code == 409


def test_me_returns_current_user_with_token(client: TestClient):
    payload = register_payload()

    register_response = client.post("/api/v1/auth/register", json=payload)
    assert register_response.status_code == 200

    token = register_response.json()["access_token"]

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == 200

    data = me_response.json()

    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert "password_hash" not in data


def test_me_rejects_missing_token(client: TestClient):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_login_rejects_wrong_password(client: TestClient):
    payload = register_payload()

    register_response = client.post("/api/v1/auth/register", json=payload)
    assert register_response.status_code == 200

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": payload["email"],
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
