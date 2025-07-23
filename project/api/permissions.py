from api.auth import get_current_user
from database.settings import get_db
from database.models.users import User
from database.models.social_network import SocialNetwork
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from api.exceptions.error_404 import SocialNetworkNotFound
from api.exceptions.error_403 import NotRightsForUpdateSN


async def permisson_for_update_social_network(
        social_network_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
):
    social_network = await session.get(SocialNetwork, social_network_id)

    if not social_network:
        raise SocialNetworkNotFound(
            social_network_id=social_network_id
        )

    if social_network.user_id != current_user.id:
        raise NotRightsForUpdateSN()

    return social_network
