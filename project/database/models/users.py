from database.models import Model
from passlib.context import CryptContext
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Model):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    manual_update: Mapped[bool] = mapped_column(Boolean, default=False)
    social_networks = relationship(
        "SocialNetwork", back_populates="user"
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    async def set_password(self, password: str):
        self.password = context.hash(password)

    async def check_password(self, password: str):
        return context.verify(password, self.password)
