from logging import Logger, getLogger

from core.settings import Settings
from store.accessors.accessor import Accessor
from store.base import BaseConnection
from store.database.database import Database
from store.managers.manager import Manager


class Store(BaseConnection):
    """Класс-хранилище для приложения."""

    def __init__(self, settings: "Settings", logger: Logger = getLogger(__name__)):
        # Подключение к базам данных
        self.db = Database(settings, logger)
        # Ассессоры, для работы с базами данных (Создание, чтение, обновление, удаление)
        self.accessor = Accessor(settings, self.db, logger)
        # Менеджеры, для работы логикой приложения (Создание, чтение, обновление, удаление)
        self.manager = Manager(settings, self.db, self.accessor, logger)
