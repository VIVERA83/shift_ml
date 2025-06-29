from logging import Logger, getLogger

from core.settings import Settings
from store.base import BaseConnection
from store.database.postgres.accessor import PostgresAccessor
from store.database.redis_db.accessor import RedisAccessor


class Database(BaseConnection):
    """Класс работы с базами данных."""

    def __init__(self, settings: "Settings", logger: Logger = getLogger(__name__)):
        self.postgres = PostgresAccessor(settings.postgres, logger)
        self.redis = RedisAccessor(settings.redis, logger)
