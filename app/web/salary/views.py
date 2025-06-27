from typing import Optional

from fastapi import APIRouter, Request

from core.lifespan import store
from .schema import SalarySchema, DateSchema

salary_route = APIRouter(prefix="/salary", tags=["SALARY"])


@salary_route.post(
    "",
    summary="Зарплата",
    description="Добавить дату повышения зарплаты и новое значение зарплаты.",
    response_model=SalarySchema,
)
async def create_salary(salary_data: SalarySchema):
    return await store.salary_accessor.create(**salary_data.model_dump())


@salary_route.get(
    "",
    summary="Текущая зарплата",
    description="Получить текущую зарплату пользователя. ",
    response_model=SalarySchema,
)
async def get_current_salary(request: Request):
    return await store.salary_accessor.get_current_salary(1)


@salary_route.get(
    "/next_date_change",
    summary="Дата следующего повышения зарплаты",
    description="Получить дату следующего повышения зарплаты. ",
    response_model=Optional[DateSchema],
)
async def next_date_change():
    return await store.salary_accessor.get_next_date_change(1)
