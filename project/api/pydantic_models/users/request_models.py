from api.pydantic_models.users.base_models import BaseUser
from api.utils import ValidationPasswordError, validate_password
from pydantic import BaseModel, Field, field_validator


class UserPasswordRequest(BaseModel):
    """Модель обновления пароля"""
    current_password: str = Field(examples=["Aezakmi321"])
    new_password: str = Field(examples=["Hesoyam123"])

    @field_validator("new_password")
    def check_password(cls, value: str):
        try:
            validate_password(value)
        except ValidationPasswordError as e:
            raise ValueError(str(e))
        return value


class UserCreate(BaseUser):
    """Модель создания пользователя"""
    password: str = Field(examples=["Aezakmi321"])

    @field_validator("password")
    def check_password(cls, value: str):
        try:
            validate_password(value)
        except ValidationPasswordError as e:
            raise ValueError(str(e))
        return value


class UserUpdate(BaseUser):
    """Модель обновления данных пользователя"""
    pass
