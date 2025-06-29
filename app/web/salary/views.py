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
    return await store.accessor.salary.create(**salary_data.model_dump())


@salary_route.get(
    "",
    summary="Текущая зарплата",
    description="Получить текущую зарплату пользователя. ",
    response_model=Optional[SalarySchema],
)
async def get_current_salary(request: Request):
    return await store.accessor.salary.get_current_salary(int(request.state.user_id))


@salary_route.get(
    "/next_date_change",
    summary="Дата следующего повышения зарплаты",
    description="Получить дату следующего повышения зарплаты. ",
    response_model=Optional[DateSchema],
)
async def next_date_change(request: Request):
    return await store.accessor.salary.get_next_date_change(int(request.state.user_id))
