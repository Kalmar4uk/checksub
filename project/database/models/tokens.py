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

    pass


class BlackListRefreshToken(BaseRefreshToken):
    __tablename__ = "blacklistrefreshtoken"

    pass


class BlackListAccessToken(Model):
    __tablename__ = "blacklistaccesstoken"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    access_toren: Mapped[str] = mapped_column(String(400), unique=True)
