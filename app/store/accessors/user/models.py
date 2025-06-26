from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column
from store.database.postgres.base import Base, BaseModel


@dataclass
class UserModel(Base, BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    @property
    def to_dict(self) -> dict:
        """Возвращает данные пользователя, без пароля."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
