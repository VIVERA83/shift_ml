from fastapi import FastAPI
from fastapi.applications import AppType
from fastapi.staticfiles import StaticFiles

from admin.setup import setup_admin
from core.lifespan import lifespan
from core.middelware import setup_middleware
from core.routes import setup_routes
from core.settings import Settings
from core.swagger import setup_openapi
from logger.logger import CustomLogger


def setup() -> "AppType":
    settings = Settings()
    logger = CustomLogger()
    app = FastAPI(lifespan=lifespan, )
    app.mount("/static", StaticFiles(directory="static"), name="static")
    setup_admin(app, settings.auth.secret_key)
    setup_middleware(app, logger)
    setup_routes(app)
    setup_openapi(app)
    return app
