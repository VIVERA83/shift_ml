from logging import Logger, getLogger

from core.settings import Settings
from store.accessors.accessor import Accessor
from store.base import BaseConnection
from store.database.database import Database


class Manager(BaseConnection):
    """Класс работы с менеджерами."""

    def __init__(
            self,
            settings: Settings,
            db: "Database",
            accessors: Accessor,
            logger: Logger = getLogger(__name__),
    ):
        ...
