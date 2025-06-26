from logging import Logger, getLogger

from core.settings import Settings
from store.accessors.salary.accessor import SalaryAccessor
from store.accessors.user.accessor import UserAccessor
from store.database.database import Database


class Store:
    """Класс-хранилище для приложения."""

    def __init__(self, settings: "Settings", logger: Logger = getLogger(__name__)):
        self.database = Database(settings, logger)

        # Классы для работы с БД
        self.user_accessor = UserAccessor(self.database.postgres, logger)
        self.salary_accessor = SalaryAccessor(self.database.postgres, logger)

    async def connect(self, *_, **__):
        await self.database.connect()

    async def disconnect(self, *_, **__):
        await self.database.disconnect()
