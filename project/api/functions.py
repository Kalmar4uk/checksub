from api.exceptions.error_404 import UserNotFound
from api.pydantic_models.social_networks.response_models import \
    SocialNetworkResponse
from api.pydantic_models.users.response_models import \
    UserResponseWithSocialNetwork
from database.models.users import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def get_user_social_networks(
        user_id: int,
        session: AsyncSession
):
    query = select(User).where(
        User.id == user_id
    ).options(
        selectinload(User.social_networks)
    )
    result = await session.execute(query)
    user = result.scalar()
    if not user:
        raise UserNotFound(user_id=user_id)

    social_networks = await return_user_social_networks(user=user)

    return UserResponseWithSocialNetwork.from_orm(
        model=user, social_networks=social_networks
    )


async def return_user_social_networks(user: User):
    social_networks = [
        SocialNetworkResponse.from_orm(
            model=sn,
        ) for sn in user.social_networks
    ]

    return social_networks
