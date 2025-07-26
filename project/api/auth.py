from datetime import datetime, timedelta

import jwt
import settings
from api.exceptions.error_401 import NotAuth, NotValidToken
from api.exceptions.error_403 import NotRights
from api.exceptions.error_404 import UserNotFound
from database.models.users import User
from database.models.tokens import BlackListAccessToken
from database.settings import get_db
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "admin": "full access"
    },
    auto_error=False
)


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode: dict = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(
        to_encode,
        settings.SECRET_KEY_JWT,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_access_and_refresh_tokens(data: dict) -> str:
    data_for_access: dict = data.copy()
    data_for_access.update(token_type="access_token")
    exp_access_token = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data_for_access,
        expires_delta=exp_access_token
    )

    data_for_refresh: dict = data.copy()
    data_for_refresh.update(token_type="refresh_token")
    exp_refresh_token = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_token(
        data_for_refresh,
        expires_delta=exp_refresh_token
    )

    return access_token, refresh_token


async def check_access_token(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_db)
) -> dict:
    """Поиск и чтение токена"""
    if not token:
        raise NotAuth()
    try:
        payload: dict = jwt.decode(
            token,
            settings.SECRET_KEY_JWT,
            algorithms=[settings.ALGORITHM]
        )
    except InvalidTokenError:
        raise NotValidToken()

    query = await session.execute(
        select(exists().where(BlackListAccessToken.access_token == token))
    )
    if query.scalar():
        raise NotValidToken()

    return payload


async def get_current_user(
        scopes: SecurityScopes,
        payload: dict = Depends(check_access_token),
        session: AsyncSession = Depends(get_db)
) -> User:
    """Проверка токена пользователя"""

    email: str = payload.get("sub")
    if not email:
        raise NotValidToken()
    token_scopes: str = payload.get("scopes", [])
    if scopes.scopes:
        for scope in scopes.scopes:
            if scope not in token_scopes:
                raise NotRights()
    try:
        query = await session.execute(select(User).filter_by(email=email))
        user = query.scalar()
    except Exception:
        raise UserNotFound(email=email)

    return user
