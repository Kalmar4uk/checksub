from pydantic import BaseModel, Field


class BaseToken(BaseModel):
    """Модель токенов"""
    access_token: str = Field(examples=["dfsadfasfsdfsdfsd.ewqeqwe1213"])
    refresh_token: str = Field(examples=["ipoieopwqensbadsad.sdawe123"])
    token_type: str = Field(examples=["Bearer"])
