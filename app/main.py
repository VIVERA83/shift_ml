import uvicorn
from core.settings import UvicornSettings

if __name__ == "__main__":
    settings = UvicornSettings()
    uvicorn.run(
        app="core.setup:setup",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        log_level=settings.log_level.lower(),
        reload=settings.reload,
    )
