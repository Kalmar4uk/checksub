from api.pydantic_models.users.request_models import UserPasswordRequest
from pydantic import BaseModel, Field, field_validator


class UserLogin(BaseModel):
    """Модель для получения токена"""
    email: str = Field(examples=["puska@mail.ru"])
    password: str = Field(examples=["Aezakmi321"])
