from api.auth import get_current_user
from api.exceptions.error_500 import ExceptionSaveDataBase
from api.functions import get_user_social_networks, return_user_social_networks
from api.pydantic_models.users.request_models import UserCreate
from api.pydantic_models.users.response_models import (
    UserResponse, UserResponseWithSocialNetwork)
from api.pydantic_models.social_networks.response_models import SocialNetworkResponce
from api.pydantic_models.social_networks.request_models import SocialNetworkForCreate
from api.routers.routers import router_social_network
from api.utils import check_unique_email
from database.models.users import User
from database.models.social_network import SocialNetwork
from database.settings import get_db
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


@router_social_network.post("/", response_model=list[SocialNetworkResponce])
async def create_social_network(
    form_data: list[SocialNetworkForCreate],
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    result = []
    for sn in form_data:
        social_network = SocialNetwork(type=sn.type, username_network=sn.username_network, user_id=current_user.id)
        session.add(social_network)
        result.append(social_network)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)

    return [SocialNetworkResponce.from_orm(model=sn) for sn in result]
