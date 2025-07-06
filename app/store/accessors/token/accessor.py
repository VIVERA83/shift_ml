from datetime import timedelta, datetime, timezone
from logging import getLogger, Logger
from typing import Optional

from jose import jwt, JWSError
from passlib.context import CryptContext

from core.settings import AuthSettings
from store.database.redis_db.accessor import RedisAccessor


class TokenAccessor:

    def __init__(
        self,
        settings: AuthSettings,
        redis: RedisAccessor,
        logger: Logger = getLogger("TokenAccessor"),
    ):
        self.settings = settings
        self.redis = redis
        self.logger = logger
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_token(self, data: dict, expires_delta: timedelta):
        """Генерация JWT токена."""
        to_encode = data.copy()

        # Используем актуальный метод для получения UTC времени
        expire = datetime.now(timezone.utc) + expires_delta

        # Конвертируем в UTC без timezone (как ожидает JWT стандарт)
        expire = expire.replace(tzinfo=None)

        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode, self.settings.secret_key, algorithm=self.settings.algorithm
        )

    def create_access_token(self, user_id: str):
        """Генерация Access Token (короткоживущий)."""
        return self.create_token(
            {
                "sub": user_id,
                "type": "access",
            },
            expires_delta=timedelta(minutes=self.settings.access_token_expire_minutes),
        )

    async def create_refresh_token(self, user_id: str):
        """Генерация Refresh Token (долгоживущий)."""
        refresh_token = self.create_token(
            {"sub": user_id, "type": "refresh"},
            expires_delta=timedelta(days=self.settings.refresh_token_expire_days),
        )

        # Вычисляем срок действия в секундах
        expire_seconds = self.settings.refresh_token_expire_days * 24 * 60 * 60

        await self.redis.set(f"refresh:{user_id}", refresh_token, expire_seconds)
        return refresh_token

    def verify_password(self, password: str, password_hash: str) -> bool:
        return self.pwd_context.verify(password, password_hash)

    # Проверка токена
    def verify_token(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(
                token=token,
                key=self.settings.secret_key,
                algorithms=self.settings.algorithm,
            )
        except JWSError as e:
            self.logger.error(e, exc_info=True, stack_info=True)
        except Exception as e:
            if self.logger:
                self.logger.exception(f"Не удалось декодировать токен: {e}")
        return None

    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Token expired or invalid")

    # Проверка refresh-токена
    def verify_refresh_token(self, token: str):
        # try:
        payload = jwt.decode(
            token, self.settings.secret_key, algorithms=[self.settings.algorithm]
        )
        # if payload.get("type") != "refresh":
        #     raise HTTPException(status_code=401, detail="Not a refresh token")

        user_id = payload.get("sub")
        stored_token = self.redis.get(f"refresh:{user_id}")

        # if not stored_token or stored_token.decode() != token:
        #     raise HTTPException(status_code=401, detail="Refresh token revoked")

        return user_id

    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Invalid refresh token")
