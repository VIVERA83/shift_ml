from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field
from datetime import date


class DateSchema(BaseModel):
    date: Annotated[date, Field(description="Дата события")]


class SalarySchema(DateSchema):
    salary: Annotated[Decimal, Field(description="зарплата", examples=["174000.00"])]
    user_id: int = Field(description="идентификатор пользователя", examples=[1])
