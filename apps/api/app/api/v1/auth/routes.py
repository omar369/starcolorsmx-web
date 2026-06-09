from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.api.v1.auth.models import User
from app.api.v1.auth.schemas import TokenResponse, UserLogin, UserPublic, UserRegister
from app.api.v1.auth.security import create_access_token, decode_access_token
from app.api.v1.auth.service import authenticate_user, create_user, get_user_by_id
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

bearer_scheme = HTTPBearer()

DbSession = Annotated[Session, Depends(get_db)]
BearerCredentials = Annotated[
    HTTPAuthorizationCredentials,
    Depends(bearer_scheme),
]


def get_current_user(
    credentials: BearerCredentials,
    db: DbSession,
) -> User:
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        ) from None

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    return user


@router.post("/register", response_model=TokenResponse)
def register_user(
    data: UserRegister,
    db: DbSession,
) -> TokenResponse:
    user = create_user(db, data)
    token = create_access_token(subject=str(user.id))

    return TokenResponse(
        access_token=token,
        user=UserPublic.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login_user(
    data: UserLogin,
    db: DbSession,
) -> TokenResponse:
    user = authenticate_user(db, data.email, data.password)
    token = create_access_token(subject=str(user.id))

    return TokenResponse(
        access_token=token,
        user=UserPublic.model_validate(user),
    )


CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/me", response_model=UserPublic)
def get_me(
    current_user: CurrentUser,
) -> User:
    return current_user
