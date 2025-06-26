from fastapi import APIRouter, Request
from icecream import ic

from core.lifespan import store
from .schema import BaseSalarySchema

salary_route = APIRouter(prefix="/salary", tags=["SALARY"])


@salary_route.post(
    "",
    summary="Зарплата",
    description="Добавить дату повышения зарплаты и новое значение зарплаты.",
    response_model=BaseSalarySchema,
)
async def create_salary(salary_data: BaseSalarySchema):
    return await store.salary_accessor.create(**salary_data.model_dump())


@salary_route.get("", response_model=BaseSalarySchema)
async def get_current_salary(request: Request):
    salary = await store.salary_accessor.get_current_salary(1)
    ic(salary)
    return salary or []
