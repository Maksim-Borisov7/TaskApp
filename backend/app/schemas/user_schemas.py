from pydantic import EmailStr, BaseModel, Field


class UserRegistrationSchema(BaseModel):
    """
    Схема для регистрации пользователя.

    Наследует UsersAuthSchema и добавляет имя пользователя.

    Attributes:
        email (EmailStr): Email пользователя.
        password (str): Пароль пользователя, от 3 до 15 символов.
        username (str): Имя пользователя, от 3 до 20 символов.
    """
    email: EmailStr
    password: str = Field(..., min_length=3, max_length=20, description="Пароль от 3 до 15 символов")
    username: str = Field(..., min_length=3, max_length=20, description="Имя пользователя от 3 до 20 символов")


class TokenInfo(BaseModel):
    """
    Схема для ответа с JWT-токеном.

    Attributes:
        access_token (str): JWT-токен доступа.
        token_type (str): Тип токена.
    """
    access_token: str
    token_type: str
