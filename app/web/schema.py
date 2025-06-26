from uuid import UUID

from pydantic import BaseModel, field_validator, Field, EmailStr, model_validator


class BaseUserSchema(BaseModel):
    username: str = Field(description="имя пользователя", examples=["Миронов Иван Иванович"])
    email: EmailStr = Field(description="email пользователя", examples=["test@test.com"])


class CreateUserSchema(BaseUserSchema):
    password: str = Field(description="пароль, должен быть не менее 8 символов", examples=["test_password"])
    password_confirm: str = Field(description="подтверждение пароля", examples=["test_password"])

    @model_validator(mode='after')
    def validate_passwords_match(self) -> 'CreateUserSchema':
        if self.password != self.password_confirm:
            raise ValueError("Пароли не совпадают")
        return self


class UserSchema(BaseUserSchema):
    id: int = Field(description="идентификатор пользователя")
