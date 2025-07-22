import re

from pydantic import BaseModel, Field, field_validator


class BaseUser(BaseModel):
    """Базовая модель пользователя"""
    email: str = Field(examples=["puska@mail.ru"])
    first_name: str = Field(examples=["Пуси"])
    last_name: str = Field(examples=["Султан"])

    @field_validator("email")
    def check_email(cls, value: str):
        if not re.search(r"^[\w.]+@[\w]+\.+(ru|com)$", value):
            raise ValueError("Некорректный Email")
        return value
