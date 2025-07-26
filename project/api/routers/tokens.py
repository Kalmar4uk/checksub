import settings
from api.auth import get_access_and_refresh_tokens, oauth2_scheme, get_current_user
from api.exceptions.error_401 import NotValidEmailOrPassword
from api.exceptions.error_404 import UserNotFound
from api.exceptions.error_500 import ExceptionSaveDataBase
from api.pydantic_models.tokens.request_models import UserLogin
from api.pydantic_models.tokens.response_models import TokenResponse
from api.routers import router_token
from database.models.users import User
from database.models.tokens import RefreshToken, BlackListRefreshToken, BlackListAccessToken
from datetime import datetime, timedelta
from database.settings import get_db
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


@router_token.post("/login", response_model=TokenResponse)
async def login(
    from_data: UserLogin,
    session: AsyncSession = Depends(get_db)
) -> TokenResponse:
    try:
        query = await session.execute(
            select(User).filter_by(
                email=from_data.email)
            )
        user = query.scalar()
    except Exception:
        raise UserNotFound(email=from_data.email)
    if not await user.check_password(from_data.password):
        raise NotValidEmailOrPassword()

    data = {"sub": user.email}
    if user.is_admin:
        data["scopes"] = "admin"

    access_token, refresh_token = get_access_and_refresh_tokens(
        data=data
    )

    exp_refresh_token = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_token_db = RefreshToken(
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=datetime.now()+exp_refresh_token
    )

    session.add(refresh_token_db)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )


@router_token.post("/logout", status_code=204)
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    await session.refresh(current_user, ["refresh_token"])

    for refresh in current_user.refresh_token:
        black_refresh = BlackListRefreshToken(
            user_id=refresh.user_id,
            refresh_token=refresh.refresh_token,
            expires_at=refresh.expires_at
        )
        session.add(black_refresh)
        await session.delete(refresh)

    access = BlackListAccessToken(
        user_id=current_user.id,
        access_token=token
    )

    session.add(access)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)
