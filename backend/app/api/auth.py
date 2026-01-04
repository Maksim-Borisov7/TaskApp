from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.dependencies.use_cases import get_create_user_use_case, get_auth_user_use_case
from backend.app.logs.logger import logger
from backend.app.schemas.user_schemas import UserRegistrationSchema, TokenInfo
from backend.app.use_case.auth_user import AuthUserUseCase
from backend.app.use_case.create_user import CreateUserUseCase

router = APIRouter(prefix='/auth', tags=["authentication"])


@router.post("/registration/", summary="Регистрация пользователя")
async def registration(
    credentials: UserRegistrationSchema,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
) -> dict:
    """
    Регистрация нового пользователя.

    Проверяет корректность введённых данных, хэширует пароль
    и сохраняет нового пользователя в базе данных.

    Args:
        credentials (UserRegistrationSchema): Данные для регистрации (username, email, password).
        use_case (CreateUserUseCase): Use-case для создания пользователя.
            Получается через Depends.

    Returns:
        dict: Сообщение об успешной регистрации.
    """
    logger.info("Регистрация пользователя")
    return await use_case.execute(credentials)


@router.post("/login/", summary="Авторизация пользователя", response_model=TokenInfo)
async def auth_user(
    form: OAuth2PasswordRequestForm = Depends(),
    use_case: AuthUserUseCase = Depends(get_auth_user_use_case),
) -> TokenInfo:
    """
    Авторизация пользователя и генерация JWT-токена.

    Проверяет логин и пароль пользователя и возвращает access token.

    Args:
        form (OAuth2PasswordRequestForm): Стандартная форма OAuth2 с полями username и password.
        use_case (AuthUserUseCase): Use-case для аутентификации пользователя.

    Returns:
        TokenInfo: Информация о токене, включает:
            - access_token: сам JWT-токен
            - token_type: тип токена
    """
    logger.info("Авторизация пользователя")
    return await use_case.execute(form.username, form.password)
