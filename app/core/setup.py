from fastapi import FastAPI
from fastapi.applications import AppType


from core.lifespan import lifespan
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
    # app.settings = settings
    # setup_logging(app)
    # setup_store(app)
    # setup_middleware(app)
    setup_routes(app)
    logger.info(f"Swagger link: ")
    return app