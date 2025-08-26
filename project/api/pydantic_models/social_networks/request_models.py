from api.constants import TYPE_SN
from pydantic import BaseModel, Field, field_validator


class SocialNetworkForCreate(BaseModel):
    """Модель для добавления социальной сети"""
    title: str = Field(
        examples=["YouTube"],
        description=(
            "Поле принимает тип социальной сети "
            "YouTube, VK, TikTok, Twitch")
    )
    username_network: str = Field(examples=["puskacause"])

    @field_validator("title")
    def check_title(value: str):
        if value not in TYPE_SN:
            raise ValueError(
                "Некорректный тип социальной сети. "
                "Может быть только: "
                "YouTube, VK, TikTok, Twitch"
            )
        return value
