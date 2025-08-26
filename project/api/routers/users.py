from api.auth import get_current_user
from api.exceptions.error_404 import UserNotFound
from api.exceptions.error_500 import ExceptionSaveDataBase
from api.functions import get_user_social_networks, return_user_social_networks
from api.pydantic_models.users.request_models import (UserCreate,
                                                      UserPasswordRequest)
from api.pydantic_models.users.response_models import (
    UserResponse, UserResponseWithSocialNetwork)
from api.routers.routers import router_user
from api.utils import check_unique_email
from database.models.users import User
from database.settings import get_db
from fastapi import Depends, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


@router_user.post("/", response_model=UserResponse)
async def create_user(
    form_data: UserCreate,
    session: AsyncSession = Depends(get_db)
) -> UserResponse:

    await check_unique_email(session=session, email=form_data.email)

    user = User(**form_data.model_dump())

    session.add(user)
    await user.set_password()

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)

    return UserResponse.from_orm(model=user)


@router_user.get("/me", response_model=UserResponseWithSocialNetwork)
async def user_me(
    user: UserResponseWithSocialNetwork = Depends(get_user_social_networks)
):
    return user


@router_user.get("/{user_id}", response_model=UserResponseWithSocialNetwork)
async def get_user(
    user: UserResponseWithSocialNetwork = Depends(get_user_social_networks)
):
    return user


@router_user.get("/", response_model=list[UserResponseWithSocialNetwork])
async def get_users(
    username: str = Query("all", description="Указать логин пользователя"),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if username == "all":
        query = await session.execute(
            select(User).options(
                selectinload(User.social_networks)
            )
        )
        result = query.scalars().all()
    else:
        query = await session.execute(
            select(User).options(
                selectinload(User.social_networks)
            ).where(User.email == username)
        )
        result = query.scalar()

        if not result:
            raise UserNotFound(email=username)

    return [
        UserResponseWithSocialNetwork.from_orm(
            user,
            social_networks=await return_user_social_networks(user=user)
        ) for user in result
    ]


@router_user.patch("/set_password", status_code=204)
async def set_password(
    form_data: UserPasswordRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    await current_user.check_password(form_data.current_password)
    current_user.password = form_data.new_password
    await current_user.set_password()

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)
