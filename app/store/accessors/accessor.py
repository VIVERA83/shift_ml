from logging import Logger, getLogger

from core.settings import Settings
from store.accessors.salary.accessor import SalaryAccessor
from store.accessors.token.accessor import TokenAccessor
from store.accessors.user.accessor import UserAccessor
from store.base import BaseConnection
from store.database.database import Database


class Accessor(BaseConnection):
    """Класс работы с ассессорами."""

    def __init__(self, settings: "Settings", db: "Database", logger: Logger = getLogger(__name__)):
        self.user = UserAccessor(settings.admin, accessor=db.postgres, loger=logger)
        self.salary = SalaryAccessor(db.postgres, logger)
        self.token = TokenAccessor(settings.auth, db.redis, logger)
