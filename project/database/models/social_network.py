from datetime import datetime

from database.models import Model
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class BaseSocialNetword(Model):
    __abstract__ = True

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    username_network: Mapped[str] = mapped_column(String(150), unique=True)
    followers_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    likes_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class YouTube(BaseSocialNetword):
    __tablename__ = "youtube"

    user = relationship("User", back_populates="youtube")


class VK(BaseSocialNetword):
    __tablename__ = "vk"

    user = relationship("User", back_populates="vk")
