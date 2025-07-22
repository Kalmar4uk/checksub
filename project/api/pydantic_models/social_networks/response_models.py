from api.pydantic_models.core import Base
from api.pydantic_models.social_networks.base_models import BaseSocialNetwork
from pydantic import Field


class SocialNetworkWithUser(Base, BaseSocialNetwork):
    """Модель социальной сети для ответа с пользователем"""

    @classmethod
    def from_orm(cls, model):
        return cls(
            id=model.id,
            type=model.type,
            username_network=model.username_network,
            followers_count=model.followers_count,
            likes_count=model.likes_count
        )


class SocialNetworkResponce(SocialNetworkWithUser):
    """Модель социальной сети для ответа"""
    username_network: str = Field(examples=["puskacause"])
