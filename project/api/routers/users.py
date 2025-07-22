from api.auth import get_current_user
from api.exceptions.error_500 import ExceptionSaveDataBase
from api.functions import get_user_social_networks, return_user_social_networks
from api.pydantic_models.users.request_models import UserCreate
from api.pydantic_models.users.response_models import (
    UserResponse, UserResponseWithSocialNetwork)
from api.routers.routers import router_user
from api.utils import check_unique_email
from database.models.users import User
from database.settings import get_db
from fastapi import Depends
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
    password = user.password
    await user.set_password(password)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)

    return UserResponse.from_orm(model=user)


@router_user.get("/me", response_model=UserResponseWithSocialNetwork)
async def user_me(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_user_social_networks(
        user_id=current_user.id,
        session=session
    )


@router_user.get("/", response_model=list[UserResponseWithSocialNetwork])
async def get_users(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(User).options(
        selectinload(User.youtube),
        selectinload(User.vk)
    )
    users = await session.execute(query)

    return [
        UserResponseWithSocialNetwork.from_orm(
            user,
            social_networks=await return_user_social_networks(user=user)
        ) for user in users.scalars().all()
    ]


@router_user.get("/{user_id}", response_model=UserResponseWithSocialNetwork)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_user_social_networks(
        user_id=user_id,
        session=session
    )
