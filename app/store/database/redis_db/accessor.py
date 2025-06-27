from store.database.postgres.accessor import BaseAccessor


class RedisAccessor(BaseAccessor):

    async def set(self, name: str, value: str | None, expires: int) -> bool:
        return await self.app.redis.connector.set(
            name=name, value=value, ex=expires
        )  # noqa

    async def get(self, name: str) -> str | dict | None:
        return await self.app.redis.connector.get(name=name)

    async def ttl(self, name: str) -> int:
        """Get a lifetime.

        Args:
            name: The name of the cache

        Returns:
            obj: The lifetime in seconds, if not found return -2, if timeless return -1
        """

        return await self.app.redis.connector.ttl(name=name)

    async def delete(self, name: str) -> bool:
        """Delete one or more keys specified by 'names'.

        Args:
            name: The name of the cache
        """
        return await self.app.redis.connector.delete(name)
