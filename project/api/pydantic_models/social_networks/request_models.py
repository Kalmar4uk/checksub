from pydantic import BaseModel, Field, field_validator
from api.constants import TYPE_SN


class SocialNetworkForCreate(BaseModel):
    """Модель для добавления социальной сети"""
    type: str = Field(
        examples=["Y"],
        description=(
            "Поле принимает тип социальной сети "
            "Y - YouTube, V - Vkontakte, TT - TikTok, TW - Twich")
    )
    username_network: str = Field(examples=["puskacause"])

    @field_validator("type")
    def check_type(value: str):
        if value not in TYPE_SN:
            raise ValueError(
                "Некорректный тип социальной сети. "
                "Может быть только: "
                "Y - YouTube, V - Vkontakte, TT - TikTok, TW - Twich"
            )
        return value
