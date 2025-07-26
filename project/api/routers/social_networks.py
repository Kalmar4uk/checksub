from api.auth import get_current_user
from api.exceptions.error_500 import ExceptionSaveDataBase
from api.functions import check_followers_or_likes_count
from api.permissions import permisson_author_social_network
from api.pydantic_models.social_networks.request_models import \
    SocialNetworkForCreate
from api.pydantic_models.social_networks.response_models import \
    SocialNetworkResponse
from api.routers.routers import router_social_network
from database.models import UserSocialNetwork
from database.models.social_network import SocialNetwork
from database.models.users import User
from database.settings import get_db
from fastapi import Depends
from sqlalchemy import select, exists
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
        query = await session.execute(
            select(SocialNetwork).where(
                SocialNetwork.username_network == sn.username_network
            )
        )
        if not (social_network := query.scalar()):
            social_network = SocialNetwork(
                title=sn.title,
                username_network=sn.username_network
            )
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
            session.add_all([association, social_network])
        result.append(social_network)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ExceptionSaveDataBase(error=e)

    return [SocialNetworkResponse.from_orm(model=sn) for sn in result]


# Пока под вопросом, нужно обсудить
# Вероятно роут пойдет *****
# На текущий момент не адаптирован под новую таблицу
# Использование скорее всего даст ошибку
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


# Изменить удаление
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
