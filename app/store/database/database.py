from logging import Logger, getLogger

from core.settings import Settings
from store.database.postgres.accessor import PostgresAccessor


class Database:
    """Класс работы с базами данных."""

    def __init__(self, settings: "Settings", logger: Logger = getLogger(__name__)):
        self.postgres = PostgresAccessor(settings.postgres, logger)

    async def connect(self, *_, **__):
        await self.postgres.connect()

    async def disconnect(self, *_, **__):
        await self.postgres.disconnect()
