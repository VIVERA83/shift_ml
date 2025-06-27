from fastapi import APIRouter, Depends, HTTPException
from icecream import ic

from core.lifespan import store
from web.auth.schema import UserSchema, CreateUserSchema, UserLoginSchema
from web.auth.utils import pwd_context, create_access_token, create_refresh_token

auth_route = APIRouter(prefix="/auth", tags=["AUTH"])


@auth_route.post(
    "",
    summary="Регистрация нового пользователя",
    description="Добавить нового пользователя.",
    response_model=UserSchema,
)
async def create_user(user_data: CreateUserSchema):
    user = await store.user_accessor.create(
        **user_data.model_dump(exclude={"password_confirm"})
    )
    return user.to_dict


# Логин (получение access + refresh токенов)
@auth_route.post("/login",
                 summary="Получение токенов",
                 description="Получение токенов для доступа к API",
                 response_model=UserLoginSchema,
                 )
async def login(form_data: UserLoginSchema = Depends()):
    user = await store.user_accessor.get_by_email(form_data.email)
    ic(form_data.password, user.password)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

#
# # Обновление access-токена через refresh
# @app.post("/refresh")
# async def refresh(token: str):
#     user_id = verify_refresh_token(token)
#     new_access_token = create_access_token(user_id)
#     return {"access_token": new_access_token, "token_type": "bearer"}
#
#
# # Защищенный эндпоинт
# @app.get("/me")
# async def read_me(user_id: str = Depends(verify_token)):
#     return {"user_id": user_id}
