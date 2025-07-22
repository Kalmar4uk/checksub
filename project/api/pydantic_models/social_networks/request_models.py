from pydantic import BaseModel, Field


class SocialNetworkForCreate(BaseModel):
    """Модель для добавления социальной сети"""
    type: str = Field(examples=["Y", "V"])
    username_network: str = Field(examples=["puskacause"])
