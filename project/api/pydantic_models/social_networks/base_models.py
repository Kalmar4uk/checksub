from pydantic import BaseModel, Field


class BaseSocialNetwork(BaseModel):
    """Базовая модель социальной сети"""
    title_network: str = Field(examples=["Аська"])
    followers_count: int = Field(examples=[1000])
    likes_count: int = Field(examples=[100])
