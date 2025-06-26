from fastapi import APIRouter

from core.lifespan import store
from .schema import BaseSalarySchema

salary_route = APIRouter(prefix="/salary", tags=["SALARY"])


@salary_route.post(
    "",
    summary="Зарплата",
    description="Добавить дату повышения зарплаты и новое значение зарплаты.",
    response_model=BaseSalarySchema,
)
async def create_user(salary_data: BaseSalarySchema):
    salary = await store.salary_accessor.create(**salary_data.model_dump())
    print(salary.to_dict)
    return salary
