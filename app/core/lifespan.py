from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.settings import Settings
from logger.logger import CustomLogger
from store.store import Store

# Создаем логгера
custom_logger = CustomLogger()
# Подключаемся к хранилищу приложения
store = Store(Settings(), custom_logger)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await store.connect()
    yield
    await store.disconnect()
