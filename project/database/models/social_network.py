from datetime import datetime

from database.models import Model
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class SocialNetwork(Model):
    __tablename__ = "socialnetworks"

    type: Mapped[str] = mapped_column(String(2))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="social_networks")
    username_network: Mapped[str] = mapped_column(String(150))
    followers_count: Mapped[int | None] = mapped_column(
        Integer, default=0, nullable=True
    )
    likes_count: Mapped[int | None] = mapped_column(
        Integer, default=0, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint('type', 'username_network', name='uq_type_username'),
    )
