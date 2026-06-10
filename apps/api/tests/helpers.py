from uuid import uuid4


def unique_email() -> str:
    return f"user-{uuid4().hex}@testmail.com"


def register_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "full_name": "Usuario de Prueba",
        "email": unique_email(),
        "password": "PasswordSeguro123!",
        "phone": "4432455609",
    }

    payload.update(overrides)
    return payload
