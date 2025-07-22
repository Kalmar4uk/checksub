from api.exceptions.error_404 import UserNotFound
from api.pydantic_models.social_networks.response_models import \
    SocialNetworkResponce
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
        selectinload(User.youtube),
        selectinload(User.vk)
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
    youtube = [
        SocialNetworkResponce.from_orm(
            model=youtube,
            title_network="youtube"
        ) for youtube in user.youtube
    ]

    vk = [
        SocialNetworkResponce.from_orm(
            model=vk,
            title_network="vk"
        ) for vk in user.vk
    ]

    return youtube + vk
