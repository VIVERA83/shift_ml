import re
from logging import Logger, getLogger
from typing import Callable, Awaitable

from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from core.lifespan import store
from store.accessors.token.accessor import TokenAccessor

HTTP_EXCEPTIONS = {
    status.HTTP_404_NOT_FOUND: "Not Found",
    status.HTTP_400_BAD_REQUEST: "Bad Request",
    status.HTTP_401_UNAUTHORIZED: "Unauthorized",
    status.HTTP_403_FORBIDDEN: "Forbidden",
    status.HTTP_405_METHOD_NOT_ALLOWED: "Method Not Allowed",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
}

# Пути без проверки
EXCLUDED_PATHS = [
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/register",
    "/registration",
    r"^/auth/[^?#]*$",
    r"^/static/?([^?#]*)$",
    r"^/admin/?([^?#]*)$",
]


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: Logger = getLogger(__name__)):
        super().__init__(app)
        self.logger = logger

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as error:
            self.logger.error(error, exc_info=True)
            code = getattr(error, "code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            return JSONResponse(
                status_code=code,
                content=jsonable_encoder(
                    {"detail": HTTP_EXCEPTIONS.get(code), "message": str(error.args)}
                ),
            )


class CookieAuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        token_accessor: TokenAccessor,
    ):
        super().__init__(app)
        self.token_accessor = token_accessor
        self.cookie_name = "access_token"  # Имя куки, где хранится токен

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable]
    ) -> Response:
        # Проверяем, требуется ли аутентификация для пути
        for path in EXCLUDED_PATHS:
            if re.fullmatch(path, request.url.path):
                return await call_next(request)

        # Извлекаем токен из куки
        token = request.cookies.get(self.cookie_name, "")

        # Проверяем токен
        payload = self.token_accessor.verify_token(token)
        if not payload:
            # Если токен невалиден - возвращаем 401
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен доступа",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Сохраняем ID пользователя в состоянии запроса
        request.state.user_id = payload.get("sub", None)
        print(1111111111111)
        print(request.state.user_id)
        return await call_next(request)


def setup_middleware(app: FastAPI, logger: Logger = getLogger(__name__)):
    app.add_middleware(CookieAuthMiddleware, token_accessor=store.accessor.token)
    app.add_middleware(ErrorHandlingMiddleware, logger=logger)
