import asyncio


class BaseConnection:

    async def connect(self, *_, **__):
        """
        Атрибуты класса должны иметь методы connect,
        если требуется подключение либо какие-то другие действия.
        """
        await asyncio.gather(
            *[
                accessor.connect()
                for accessor in self.__dict__.values()
                if hasattr(accessor, "connect")
            ]
        )

    async def disconnect(self, *_, **__):
        """
        Атрибуты класса должны иметь методы disconnect,
        если требуется отключение либо какие-то другие действия.
        """
        await asyncio.gather(
            *[
                accessor.disconnect()
                for accessor in self.__dict__.values()
                if hasattr(accessor, "disconnect")
            ]
        )
