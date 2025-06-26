import uuid

from fastapi import APIRouter

from core.lifespan import store
from web.schema import UserSchema, CreateUserSchema

auth_route = APIRouter(prefix="/auth", tags=["AUTH"])


@auth_route.post(
    "",
    summary="Регистрация нового пользователя",
    description="Добавить нового пользователя.",
    response_model=UserSchema,
)
async def create_user(user_data: CreateUserSchema):
    user = await store.user_accessor.create(**user_data.model_dump(exclude={"password_confirm"}))
    print(user.to_dict)
    return user.to_dict
