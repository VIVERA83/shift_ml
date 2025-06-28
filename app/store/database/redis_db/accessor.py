from logging import Logger, getLogger

from redis.asyncio import Redis

from core.settings import RedisSettings


class RedisAccessor:

    def __init__(
        self, settings: RedisSettings, logger: Logger = getLogger("RedisAccessor")
    ):
        self.settings = settings
        self.logger = logger
        self._engine = Redis.from_url(
            self.settings.dsn(True),
            decode_responses=True,
        )

    async def connect(self):
        self.logger.info(f"{self.settings.dsn()} Подключился к базе данных")

    async def disconnect(self):
        await self._engine.close()
        self.logger.info("Отключился от базы данных")

    async def set(self, name: str, value: str | None, expires: int) -> bool:
        return await self._engine.set(name=name, value=value, ex=expires)  # noqa

    async def get(self, name: str) -> str | dict | None:
        return await self._engine.get(name=name)

    async def ttl(self, name: str) -> int:
        """Получить время жизни.

        :arg
            name: имя кэша

            returns:
                object: время жизни в секундах, если не найдено, возвращает -2, если безвременное, возвращает -1
        """

        return await self._engine.ttl(name=name)

    async def delete(self, name: str) -> bool:
        """Delete one or more keys specified by 'names'.

        Args:
            name: The name of the cache
        """
        return await self._engine.delete(name)
