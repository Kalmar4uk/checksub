from datetime import datetime

from pydantic import BaseModel, Field


class BaseSocialNetwork(BaseModel):
    """Базовая модель социальной сети"""
    title: str = Field(examples=["YouTube"])
    username_network: str = Field(examples=["puskacause"])
    followers_count: int | None = Field(examples=[1000])
    likes_count: int | None = Field(examples=[100])
    updated_at: datetime
