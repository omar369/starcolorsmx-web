from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.api.v1.auth.models import User
from app.api.v1.auth.schemas import TokenResponse, UserLogin, UserPublic, UserRegister
from app.api.v1.auth.security import create_access_token, decode_access_token
from app.api.v1.auth.service import authenticate_user, create_user, get_user_by_id
from app.core.rate_limit import rate_limit_login, rate_limit_register
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


def get_optional_current_user(
    request: Request,
    db: DbSession,
) -> User | None:
    token = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        parts = auth_header.split()
        if len(parts) == 2:
            token = parts[1]

    if not token:
        token = request.query_params.get("token")

    if not token:
        return None

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
        user = get_user_by_id(db, user_id)
        if user and user.is_active:
            return user
    except Exception:
        return None
    return None


@router.post("/register", response_model=TokenResponse)
def register_user(
    request: Request,
    data: UserRegister,
    db: DbSession,
) -> TokenResponse:
    rate_limit_register(request)
    user = create_user(db, data)
    token = create_access_token(subject=str(user.id))

    return TokenResponse(
        access_token=token,
        user=UserPublic.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login_user(
    request: Request,
    data: UserLogin,
    db: DbSession,
) -> TokenResponse:
    rate_limit_login(request)
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
