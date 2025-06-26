from dataclasses import asdict, dataclass

from core.settings import PostgresSettings
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


@dataclass
class Base(DeclarativeBase):
    metadata = MetaData(
        schema=PostgresSettings().postgres_schema,
        quote_schema=True,
    )
    __table_args__ = {"extend_existing": True}

    @property
    def to_dict(self) -> dict:
        return asdict(self)  # noqa type: ignore


@dataclass
class BaseModel:
    id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )

    def __repr__(self):
        return "{class_name}(id={id})".format(
            id=self.id,
            class_name=self.__class__.__name__,
        )

    __str__ = __repr__
