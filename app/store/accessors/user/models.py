from datetime import date
from dataclasses import dataclass

from passlib.context import CryptContext
from sqlalchemy import TypeDecorator, String, Date, text, func
from sqlalchemy.orm import Mapped, mapped_column

from store.database.postgres.base import Base, BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USER_ROLES = ["admin", "user"]


class PasswordHash(TypeDecorator):
    impl = String(128)

    def process_bind_param(self, value, dialect) -> str:
        """Вызывается при сохранении в БД."""
        return pwd_context.hash(value) if value else None

    def process_result_value(self, value, dialect) -> str:
        """Вызывается при загрузке из БД."""
        return value


class Role(TypeDecorator):
    impl = String(28)

    def process_bind_param(self, value, dialect) -> str:
        """Вызывается при сохранении в БД."""
        if value not in USER_ROLES:
            raise ValueError(
                f"Недопустимое значение роли: {value}. Допустимые значения: {USER_ROLES}"
            )
        return value

    def process_result_value(self, value, dialect) -> str:
        """Вызывается при загрузке из БД."""
        return value


@dataclass
class UserModel(Base, BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(PasswordHash)
    role: Mapped[str] = mapped_column(Role, nullable=False, default="user")
    created_at: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    @property
    def to_dict(self) -> dict:
        return {
            **super().to_dict,
            "password": "",
        }
