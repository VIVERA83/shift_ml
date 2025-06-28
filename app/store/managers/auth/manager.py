from datetime import timedelta, datetime
from logging import getLogger, Logger

from jose import jwt
from passlib.context import CryptContext

from core.settings import AuthSettings
from store.database.redis_db.accessor import RedisAccessor


class AuthManager:

    def __init__(self, settings: AuthSettings, redis: RedisAccessor,
                 logger: Logger = getLogger("AuthManager")):
        self.settings = settings
        self.redis = redis
        self.logger = logger
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_token(self, data: dict, expires_delta: timedelta):
        """Генерация JWT токена."""

        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, self.settings.secret_key, algorithm=self.settings.algorithm
        )

    def create_access_token(self, user_id: str):
        """Генерация Access Token (короткоживущий)."""

        return self.create_token(
            {"sub": user_id},
            expires_delta=timedelta(minutes=self.settings.access_token_expire_minutes),
        )

    async def create_refresh_token(self, user_id: str):
        """Генерация Refresh Token (долгоживущий)."""
        refresh_token = self.create_token(
            {"sub": user_id, "type": "refresh"},
            expires_delta=timedelta(days=self.settings.refresh_token_expire_days),
        )
        expire = self.settings.refresh_token_expire_days * 24 * 60 * 60
        await self.redis.set(f"refresh:{user_id}", refresh_token, expire)
        return refresh_token

    async def verify_password(self, password: str, password_hash: str) -> bool:
        return self.pwd_context.verify(password, password_hash)


    # Проверка токена
    def verify_token(self, token: str):
        # try:
        payload = jwt.decode(
            token, self.settings.secret_key, algorithms=[self.settings.algorithm]
        )
        user_id = payload.get("sub")
        # if not user_id:
        #     raise HTTPException(status_code=401, detail="Invalid token")
        return user_id

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
