from pydantic import BaseModel, Field


class BaseSocialNetwork(BaseModel):
    """Базовая модель социальной сети"""
    type: str = Field(examples=["Y"])
    followers_count: int | None = Field(examples=[1000])
    likes_count: int | None = Field(examples=[100])
