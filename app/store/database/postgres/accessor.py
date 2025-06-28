from functools import wraps
from logging import Logger, getLogger
from typing import Any, Callable, Literal, ParamSpec, Type, TypeVar, Union
from uuid import UUID

from asyncpg import UniqueViolationError
from sqlalchemy import delete, func, insert, select, text, update
from sqlalchemy.engine import Result
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import MappedColumn, InstrumentedAttribute
from sqlalchemy.sql.elements import TextClause

from core.settings import PostgresSettings, AdminSettings
from .exceptions import (
    DataBaseConnectionException,
    DataBaseUnknownException,
    DuplicateException,
    ExceptionBase,
    ForeignKeyException,
    InternalDatabaseException,
    NotFoundException,
)
from .types import Model, Query

_PWrapped = ParamSpec("_PWrapped")
_RWrapped = TypeVar("_RWrapped")


class PostgresAccessor:

    def __init__(
            self, settings: PostgresSettings, logger: Logger = getLogger("PostgresAccessor")
    ):
        self.settings = settings
        self.logger = logger
        self._engine = create_async_engine(
            self.settings.dsn(True),
            echo=True,
            future=True,
        )

    async def connect(self):
        self.logger.info(
            f"{self.__class__.__name__} {self.settings.dsn()} подключился к базе данных"
        )

    async def disconnect(self):
        if self._engine:
            await self._engine.dispose()

        self.logger.info(f"{self.__class__.__name__} отключился от базы данных")

    @property
    def session(self) -> AsyncSession:
        return async_sessionmaker(bind=self._engine, expire_on_commit=False)()

    @staticmethod
    def get_query_insert(model: Model, **insert_data) -> Query:
        return insert(model).values(**insert_data)

    @staticmethod
    def get_query_select_by_model(model: Model) -> Query:
        return select(model)

    @staticmethod
    def get_query_select_by_fields(
            *select_field: Union[MappedColumn, Literal["*"], InstrumentedAttribute]
    ) -> Query:
        return select(*select_field)

    @staticmethod
    def get_query_update(model: Model, **update_data) -> Query:
        return update(model).values(**update_data)

    @staticmethod
    def get_query_delete(model: Model) -> Query:
        return delete(model)

    async def query_execute(self, query: Union[Query, TextClause]) -> Result[Any]:
        async with self.session as session:
            result = await session.execute(query)
            await session.commit()
            return result

    async def query_executes(self, *query: Query) -> list[Result[Any]]:
        async with self.session as session:
            result = [await session.execute(q) for q in query]
            await session.commit()
            return result

    @staticmethod
    def get_query_from_text(smtp: str) -> TextClause:
        return text(smtp)

    @staticmethod
    def get_query_random(model: Model, count: int = 1) -> Query:
        return select(model).order_by(func.random()).limit(count)


class BaseAccessor:
    class Meta:
        model: Model
        not_found: Type[ExceptionBase]
        duplicate: Type[ExceptionBase]
        foreign_key: Type[ExceptionBase]
        inner: Type[ExceptionBase]

    def __init__(self, accessor: PostgresAccessor, loger: Logger):
        self.__accessor = accessor
        self.__init_meta_class()
        self.logger = loger
        self.logger.info(f"{self.__class__.__name__} инициализирован.")

    def __init_meta_class(self):
        try:
            self.model = getattr(self.Meta, "model")
        except AttributeError:
            self.logger.error(f"Не указан класс модели {self.__class__.__name__}")
            # raise AttributeError(f"Не указан класс модели {self.__class__.__name__}")

        self.not_found = (
            self.Meta.not_found
            if getattr(self.Meta, "not_found", None)
            else NotFoundException
        )
        self.duplicate = (
            self.Meta.duplicate
            if getattr(self.Meta, "duplicate", None)
            else DuplicateException
        )
        self.foreign_key = (
            self.Meta.foreign_key
            if getattr(self.Meta, "foreign_key", None)
            else ForeignKeyException
        )
        self.inner = (
            self.Meta.inner
            if getattr(self.Meta, "inner", None)
            else InternalDatabaseException
        )

    def _exception_handler(
            self: Callable[_PWrapped, _RWrapped],
    ) -> Callable[_PWrapped, _RWrapped]:
        @wraps(self)
        async def wrapper(cls, *args, **kwargs):
            try:
                return await self(cls, *args, **kwargs)
            except (IntegrityError, NoResultFound, UniqueViolationError) as e:
                cls.logger.warning(str(e))
                if "duplicate key value violates unique constraint" in str(e):
                    raise cls.duplicate(exception=e)
                if "violates foreign key constraint" in str(e):
                    raise cls.foreign_key(exception=e)
                raise cls.not_found(exception=e)
            except IOError as e:
                cls.logger.error(str(e))
                if e.errno == 111:
                    raise DataBaseConnectionException(exception=e)
                raise DataBaseUnknownException(exception=e)
            except DBAPIError as e:
                cls.logger.error(str(e))
                raise InternalDatabaseException(exception=e)
            except Exception as e:
                cls.logger.error(str(e))
                raise DataBaseUnknownException(exception=e)

        return wrapper

    @property
    def accessor(self) -> "PostgresAccessor":
        return self.__accessor

    @_exception_handler  # noqa
    async def create(self, **fields) -> Model:
        model = self.Meta.model(**fields)
        async with self.accessor.session as session:
            session.add(model)
            await session.commit()
        self.logger.info(f"Создан {model} {model.to_dict}")
        return model

    @_exception_handler  # noqa
    async def update(self, id: int, **fields: dict) -> Model:
        smtp = (
            self.accessor.get_query_update(self.Meta.model)
            .where(self.Meta.model.id == id)  # noqa
            .values(**fields)
            .returning(self.Meta.model)
        )
        result = await self.accessor.query_execute(smtp)
        self.logger.info(f"Обновлен {self.Meta.model.__name__} с id {id}")
        return result.scalars().one()

    @_exception_handler  # noqa
    async def delete_by_id(self, id_: int | str | UUID) -> Model:
        smtp = (
            self.accessor.get_query_delete(self.Meta.model)
            .where(self.Meta.model.id == id_)  # noqa
            .returning(self.Meta.model)
        )
        result = await self.accessor.query_execute(smtp)
        self.logger.info(f"Удален {self.Meta.model.__name__} с id {id_}")
        return result.scalars().one()

    @_exception_handler  # noqa
    async def get_by_id(self, id_: int | str | UUID) -> Model:
        smtp = self.accessor.get_query_select_by_fields("*").filter(
            self.model.id == id_  # noqa
        )
        result = await self.accessor.query_execute(smtp)
        return self.Meta.model(**result.mappings().one())

    @_exception_handler  # noqa
    async def get_all(self, offset: int, limit: int) -> list[Model]:
        smtp = (
            self.accessor.get_query_select_by_model(self.Meta.model)
            .limit(limit)
            .offset(offset)
        )
        result = await self.accessor.query_execute(smtp)
        self.logger.debug(
            f"{self.__class__.__name__} get_all: {self.Meta.model.__name__} {offset=} {limit=}"
        )
        return [model[self.Meta.model.__name__] for model in result.mappings().all()]

    @_exception_handler  # noqa
    async def get_random(self, count: int) -> list[Model]:
        smtp = self.accessor.get_query_random(self.Meta.model, count)
        result = await self.accessor.query_execute(smtp)
        self.logger.debug(
            f"{self.__class__.__name__} get_random: {self.Meta.model.__name__} {count=}"
        )
        return [model[self.Meta.model.__name__] for model in result.mappings().all()]
