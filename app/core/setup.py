from fastapi import FastAPI
from fastapi.applications import AppType

from admin.setup import setup_admin
from core.lifespan import lifespan
from core.middelware import setup_middleware
from fastapi.staticfiles import StaticFiles
from core.routes import setup_routes
from logger.logger import CustomLogger



def setup() -> "AppType":

    # settings = AppSettings()
    logger = CustomLogger()
    app = FastAPI(
        lifespan=lifespan,
        # docs_url=settings.docs_url,
        # redoc_url=settings.redoc_url,
        # openapi_url=settings.openapi_url,
        # version=settings.version,
        # title=settings.title,
        # description=settings.description,
    )
    app.mount("/static", StaticFiles(directory="static"), name="static")
    # app.settings = settings
    # setup_logging(app)
    # setup_store(app)
    setup_admin(app)
    setup_middleware(app)
    setup_routes(app)
    logger.info(f"Swagger link: ")
    return app
