from datetime import datetime

from database.models import Model
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class BaseRefreshToken(Model):
    __abstract__ = True

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    refresh_token: Mapped[str] = mapped_column(String(400), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime)


class RefreshToken(BaseRefreshToken):
    __tablename__ = "refreshtoken"

    user = relationship("User", back_populates="refresh_token")


class BlackListRefreshToken(BaseRefreshToken):
    __tablename__ = "blacklistrefreshtoken"

    user = relationship("User", back_populates="black_list_refresh_token")


class BlackListAccessToken(Model):
    __tablename__ = "blacklistaccesstoken"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="black_list_access_token")
    access_token: Mapped[str] = mapped_column(String(400), unique=True)
