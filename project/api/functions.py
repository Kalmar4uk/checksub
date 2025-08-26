import json
from datetime import datetime

import requests
from api.auth import get_current_user
from api.exceptions.error_404 import SocialNetworkNotFound, UserNotFound
from api.exceptions.error_422 import CountFollowersOrLikesMoreZero
from api.exceptions.error_500 import ExceptionSaveDataBase
from api.pydantic_models.social_networks.response_models import \
    SocialNetworkResponse
from api.pydantic_models.users.response_models import \
    UserResponseWithSocialNetwork
from api.utils import get_redis
from celery_app.urls import check_user_vk, headers_vk
from database.models.social_network import SocialNetwork
from database.models.users import User
from database.settings import async_session_maker, get_db
from fastapi import Depends
from redis import Redis
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


def encoder_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


async def check_availability_social_network(
        social_network_id: int,
        session: AsyncSession = Depends(get_db),
):
    social_network = await session.get(SocialNetwork, social_network_id)

    if not social_network:
        raise SocialNetworkNotFound(
            social_network_id=social_network_id
        )

    return social_network


async def check_followers_or_likes_count(social_network: SocialNetwork):
    if (social_network.followers_count or social_network.likes_count) > 0:
        raise CountFollowersOrLikesMoreZero()


async def check_availability_user(
        user_id: int | None = None,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if user_id is None:
        return current_user

    user = await session.get(User, user_id)

    if not user:
        raise UserNotFound(user_id=user_id)

    return user


async def get_user_social_networks(
        user: User = Depends(check_availability_user),
        session: AsyncSession = Depends(get_db),
        redis: Redis = Depends(get_redis)
):
    cache_key = f"user:{user.id}:user_and_sn"
    cache = redis.get(cache_key)
    if cache:
        return json.loads(cache)

    await session.refresh(user, ["social_networks"])

    social_networks = await return_user_social_networks(user=user)

    result = UserResponseWithSocialNetwork.from_orm(
        model=user, social_networks=social_networks
    )

    redis.setex(
        cache_key,
        3600,
        json.dumps(result.model_dump(), default=encoder_datetime)
    )

    return result


async def return_user_social_networks(user: User):
    social_networks = [
        SocialNetworkResponse.from_orm(
            model=sn,
        ) for sn in user.social_networks
    ]

    return social_networks


async def check_existence(username: str, title: str):
    if title == "VK":
        if not await check_vk(username=username):
            return False
        return await get_or_create_social_network(
            username=username,
            title=title
        )


async def check_vk(username: str):
    response = requests.get(
        check_user_vk.format(username),
        headers=headers_vk
    ).json()
    if (
        not response.get("response")
        or response.get("response")[0].get("deactivated")
    ):
        return False
    return True


async def get_or_create_social_network(
        title: str,
        username: str
):
    async with async_session_maker() as session:
        query = await session.execute(
            select(SocialNetwork).where(
                SocialNetwork.title == title,
                SocialNetwork.username_network == username
            )
        )
        if (result := query.scalar()):
            return result
        else:
            social_network = SocialNetwork(
                title=title,
                username_network=username
            )
            session.add(social_network)
            try:
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise ExceptionSaveDataBase(error=e)
            return social_network
