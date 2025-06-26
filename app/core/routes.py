from fastapi import FastAPI

from web.views import auth_route


def setup_routes(app: FastAPI):
    """Настройка Роутов приложения."""
    app.include_router(auth_route)

