from fastapi import FastAPI

from web.pages.views import page_route
from web.salary.views import salary_route
from web.auth.views import auth_route


def setup_routes(app: FastAPI):
    """Настройка Роутов приложения."""
    app.include_router(auth_route)
    app.include_router(salary_route)
    app.include_router(page_route)
