import os

from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class Base(BaseSettings):
    class Config:
        env_nested_delimiter = "__"
        env_file = os.path.join(BASE_DIR, ".env")
        enf_file_encoding = "utf-8"
        extra = "ignore"


class AppSettings(BaseSettings):
    """Основные настройки приложения."""

    host: str = "127.0.0.1"
    port: int = 8081


class LogConfig(Base):
    """Настройки логирования.

    Загрузка из переменных окружения, если не указаны, то используются значения по умолчанию
    """

    level: str = "INFO"  # Уровень логирования
    filename: str = "logs/errors.log"  # Файл для записи логов


class SwaggerConfig(Base):
    """Настройки Swagger.

    Загрузка из переменных окружения, если не указаны, то используются значения по умолчанию
    """

    title: str = "API"  # Заголовок документации
    version: str = "1.0.0"  # Версия документации
    swagger_path: str = "/docs"  # URL для Swagger UI
    swagger_url: str = "/swagger.json"  # URL для Swagger JSON документации


class PostgresSettings(Base):
    """Настройки базы данных."""

    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str = "<PASSWORD>"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_schema: str = "public"

    def dsn(self, show_secret: bool = False) -> str:
        """Возвращает строку подключения к базе данных.

        :param show_secret: Если True, то пароль будет показан в строке подключения. По умолчанию False.
        """

        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
            user=self.postgres_user,
            password=(self.postgres_password if show_secret else "******"),
            host=self.postgres_host,
            port=self.postgres_port,
            db=self.postgres_db,
        )

    def __str__(self) -> str:
        """Возвращает строковое представление настроек базы данных, скрывая пароль."""

        return super().__str__().replace(self.postgres_password, "******")


class RedisSettings(Base):
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379

    def dsn(self, show_secret: bool = False) -> str:
        """Возвращает строку подключения к базе данных.

        :param show_secret: Если True, то пароль будет показан в строке подключения. По умолчанию False.
        """

        return "redis://{host}:{port}".format(
            host=self.redis_host,
            port=self.redis_port,
        )


class AuthSettings(BaseSettings):
    secret_key: str = "Life is beautiful when you smile"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7


class Settings:
    """Конфигурационные настройки всех компонентов приложения."""

    # Секция настроек логирования
    log: LogConfig = LogConfig()
    # Секция настроек Swagger
    swagger: SwaggerConfig = SwaggerConfig()
    # Секция настроек базы данных POSTGRES
    postgres: PostgresSettings = PostgresSettings()
    # Секция настроек базы данных Redis
    redis: RedisSettings = RedisSettings()

class UvicornSettings(Base):
    host: str = "127.0.0.1"
    port: int = 8081
    workers: int = 1
    log_level: str = "INFO"
    reload: bool = False
