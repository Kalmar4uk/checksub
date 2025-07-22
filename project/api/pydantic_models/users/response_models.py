from api.pydantic_models.core import Base
from api.pydantic_models.social_networks.response_models import \
    SocialNetworkWithUser
from api.pydantic_models.users.base_models import BaseUser
from pydantic import Field


class UserResponse(Base, BaseUser):
    """Модель для ответа пользователя"""
    is_admin: bool = Field(default=False, examples=[True])
    manual_update: bool = Field(default=False, examples=[False])

    @classmethod
    def from_orm(cls, model, social_networks=None):
        return cls(
            id=model.id,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            is_admin=model.is_admin,
            manual_update=model.manual_update,
            social_networks=social_networks
        )


class UserResponseWithSocialNetwork(UserResponse):
    """Модель для ответа пользователя с его социальными сетями"""
    social_networks: list[SocialNetworkWithUser] | None


class UserResponseForSocialNetwork(Base):
    """Модель пользователя для овета в социальной сети"""
    pass
