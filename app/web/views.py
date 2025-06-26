import uuid

from fastapi import APIRouter

from web.schema import UserSchema, CreateUserSchema

auth_route = APIRouter(prefix="/auth", tags=["AUTH"])


@auth_route.post(
    "",
    summary="Регистрация нового пользователя",
    description="Добавить нового пользователя.",
    response_model=UserSchema,
)
async def create_user(brand: CreateUserSchema):
    return {** brand.model_dump(exclude={"password_confirm"}) ,"id" : uuid.uuid4().hex}
