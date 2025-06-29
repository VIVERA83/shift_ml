from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from core.lifespan import store
from web.auth.schema import UserSchema, CreateUserSchema, UserLoginSchema

auth_route = APIRouter(prefix="/auth", tags=["AUTH"])


@auth_route.post(
    "/registration",
    summary="Регистрация нового пользователя",
    description="Добавить нового пользователя.",
    response_model=UserSchema,
)
async def registration(user_data: CreateUserSchema):
    return await store.accessor.user.create(
        **user_data.model_dump(exclude={"password_confirm"})
    )


@auth_route.post(
    "/login",
    summary="Получение токенов",
    description="Получение токенов для доступа к API",
    # response_model=UserLoginSchema,
)
async def login(response: Response, form_data: UserLoginSchema):
    if user := await store.accessor.user.get_by_email(form_data.email):
        if store.accessor.token.verify_password(form_data.password, user.password):
            access_token = store.accessor.token.create_access_token(user.id)
            refresh_token = await store.accessor.token.create_refresh_token(user.id)
            response.set_cookie("access_token", access_token)
            response.set_cookie("refresh_token", refresh_token)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }
        raise HTTPException(status_code=400, detail="Invalid password or email")
    raise HTTPException(status_code=400, detail="Invalid credentials")

#
# # Обновление access-токена через refresh
# @app.post("/refresh")
# async def refresh(token: str):
#     user_id = verify_refresh_token(token)
#     new_access_token = create_access_token(user_id)
#     return {"access_token": new_access_token, "token_type": "bearer"}
#
