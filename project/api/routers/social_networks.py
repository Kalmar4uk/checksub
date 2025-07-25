from api.auth import get_current_user
from api.exceptions.error_500 import ExceptionSaveDataBase
from api.functions import check_followers_or_likes_count
from api.permissions import permisson_author_social_network
from api.pydantic_models.social_networks.request_models import \
    SocialNetworkForCreate
from api.pydantic_models.social_networks.response_models import \
    SocialNetworkResponse
from api.routers.routers import router_social_network
from database.models.social_network import SocialNetwork
from database.models.users import User
from database.settings import get_db
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


@router_social_network.post("/", response_model=list[SocialNetworkResponse])
async def create_social_network(
    form_data: list[SocialNetworkForCreate],
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    result = []
    for sn in form_data:
        social_network = SocialNetwork(
            type=sn.type,
            username_network=sn.username_network,
            user_id=current_user.id
        )
        session.add(social_network)
        result.append(social_network)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)

    return [SocialNetworkResponse.from_orm(model=sn) for sn in result]


@router_social_network.put(
        "/{social_network_id}",
        response_model=SocialNetworkResponse
)
async def update_social_network(
    form_data: SocialNetworkForCreate,
    social_network: SocialNetwork = Depends(
        permisson_author_social_network
    ),
    session: AsyncSession = Depends(get_db)
):
    await check_followers_or_likes_count(social_network=social_network)

    social_network.type = form_data.type
    social_network.username_network = form_data.username_network

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)

    return SocialNetworkResponse.from_orm(social_network)


@router_social_network.delete("/{social_network_id}", status_code=204)
async def delete_social_network(
    social_network: SocialNetwork = Depends(
        permisson_author_social_network
    ),
    session: AsyncSession = Depends(get_db)
):
    try:
        await session.delete(social_network)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)
