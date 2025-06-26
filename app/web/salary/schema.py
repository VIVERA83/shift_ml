from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field
from datetime import date


class BaseSalarySchema(BaseModel):
    salary: Annotated[Decimal, Field(description="зарплата", examples=["174000.00"])]
    date: Annotated[date, Field(description="Дата события")]
    user_id: int = Field(description="идентификатор пользователя", examples=[1])
