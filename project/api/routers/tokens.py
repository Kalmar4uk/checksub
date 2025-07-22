from api.auth import get_access_and_refresh_tokens
from api.exceptions.error_401 import NotValidEmailOrPassword
from api.exceptions.error_404 import UserNotFound
from api.pydantic_models.tokens.request_models import UserLogin
from api.pydantic_models.tokens.response_models import TokenResponse
from api.routers import router_token
from database.models.users import User
from database.settings import get_db
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )
