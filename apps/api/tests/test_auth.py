from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session]:
        db = testing_session_local()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def unique_email() -> str:
    return f"user-{uuid4().hex}@testmail.com"


def register_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "full_name": "Poly Polinesa",
        "email": unique_email(),
        "password": "ChicasAlCam3rin0.69",
        "phone": "4432455609",
    }

    payload.update(overrides)
    return payload


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
