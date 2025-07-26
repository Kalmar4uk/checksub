from sqlalchemy import Integer, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Model(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UserSocialNetwork(Model):
    __tablename__ = "usersocialnetwork"

    social_network_id: Mapped[int] = mapped_column(
        ForeignKey("socialnetworks.id")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
