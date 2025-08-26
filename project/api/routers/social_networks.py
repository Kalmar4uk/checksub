from api.auth import get_current_user
from api.exceptions.error_404 import SocialNetworkNotFound
from api.exceptions.error_500 import ExceptionSaveDataBase
from api.functions import check_existence
from api.pydantic_models.social_networks.request_models import \
    SocialNetworkForCreate
from api.pydantic_models.social_networks.response_models import \
    SocialNetworkResponse
from api.routers.routers import router_social_network
from api.utils import get_redis
from database.models import UserSocialNetwork
from database.models.social_network import SocialNetwork
from database.models.users import User
from database.settings import get_db
from fastapi import Depends, Query
from redis import Redis
from sqlalchemy import delete, exists, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


@router_social_network.post("/", response_model=list[SocialNetworkResponse])
async def create_social_network(
    form_data: list[SocialNetworkForCreate],
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    result: list = []
    for sn in form_data:
        social_network = await check_existence(
            username=sn.username_network,
            title=sn.title
        )
        if not social_network:
            continue
        check_association = await session.execute(
            select(
                exists().where(
                    UserSocialNetwork.user_id == current_user.id,
                    UserSocialNetwork.social_network_id == social_network.id
                )
            )
        )
        if not check_association.scalar():
            association = UserSocialNetwork(
                user_id=current_user.id,
                social_network_id=social_network.id
            )
            session.add(association)
        result.append(social_network)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)
    if not result:
        raise SocialNetworkNotFound()
    return [SocialNetworkResponse.from_orm(model=sn) for sn in result]


@router_social_network.delete("/{social_network_id}", status_code=204)
async def delete_social_network(
    social_network_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    social_network = await session.get(SocialNetwork, social_network_id)
    check_association = await session.execute(
        select(
            exists().where(
                UserSocialNetwork.user_id == current_user.id,
                UserSocialNetwork.social_network_id == social_network.id
            )
        )
    )
    if not check_association.scalar():
        raise SocialNetworkNotFound(username=social_network.username_network)
    try:
        await session.execute(
            delete(
                UserSocialNetwork
            ).where(
                UserSocialNetwork.user_id == current_user.id,
                UserSocialNetwork.social_network_id == social_network.id
            )
        )
        await session.commit()
        redis.delete(f"user:{current_user.id}:user_and_sn")
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)


@router_social_network.get("/", response_model=SocialNetworkResponse)
async def get_social_networks(
    title: str = Query(description="YouTube, VK, TikTok, Twitch"),
    username: str = Query(description="Логин социальной сети"),
    current_user: User = Depends(get_current_user),
):
    social_network = await check_existence(
        username=username,
        title=title
    )
    if not social_network:
        raise SocialNetworkNotFound(title=title, username=username)
    return SocialNetworkResponse.from_orm(social_network)
