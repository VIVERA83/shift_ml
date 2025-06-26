from datetime import date
from dataclasses import dataclass

from sqlalchemy import Numeric, Index, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from store.database.postgres.base import Base, BaseModel


@dataclass
class SalaryModel(Base, BaseModel):
    __tablename__ = "salaries"

    salary: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date,nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    __table_args__ = (
        Index('idx_user_date', user_id, date, unique=True),
    )
