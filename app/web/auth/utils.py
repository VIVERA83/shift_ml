from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from redis import Redis

from core.settings import RedisSettings, AuthSettings

# Подключение к Redis
redis = Redis.from_url(RedisSettings().dsn())

# Настройки хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Схема OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

settings = AuthSettings()

# Генерация JWT
def create_token(data: dict, expires_delta: timedelta):

    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# Access Token (короткоживущий)
def create_access_token(user_id: str):
    return create_token(
        {"sub": user_id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


# Refresh Token (долгоживущий, сохраняется в Redis)
def create_refresh_token(user_id: str):
    refresh_token = create_token(
        {"sub": user_id, "type": "refresh"},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    redis.set(f"refresh:{user_id}", refresh_token)
    return refresh_token


# Проверка токена
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")


# Проверка refresh-токена
def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Not a refresh token")

        user_id = payload.get("sub")
        stored_token = redis.get(f"refresh:{user_id}")

        if not stored_token or stored_token.decode() != token:
            raise HTTPException(status_code=401, detail="Refresh token revoked")

        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
