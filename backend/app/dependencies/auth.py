from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from backend.app.core.jwt_utils import decode_jwt
from backend.app.core.password_utils import validate_password
from backend.app.dependencies.repositories import get_user_repo
from backend.app.repositories.users import UserRepository
from jwt.exceptions import InvalidTokenError
from backend.app.database.models import UserModels


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> dict:
    """
    Извлекает и валидирует payload JWT-токена из заголовка Authorization.

    Получает access-токен через OAuth2PasswordBearer, декодирует его
    и возвращает payload.

    Args:
        token (str): JWT-токен.

    Returns:
        dict: Payload JWT-токена.

    Raises:
        HTTPException: 401 — если токен отсутствует или невалиден.
    """

    if not token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")

    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не валидный токен"
        )
    return payload


async def get_current_auth_users(
    repo: UserRepository = Depends(get_user_repo),
    payload: dict = Depends(get_current_token_payload),
) -> UserModels:
    """
    Получает текущего аутентифицированного пользователя по JWT-токену.

    Использует payload токена для поиска пользователя в базе данных через репозиторий.
    Dependency `repo` предоставляет экземпляр UserRepository с доступной сессией базы данных.

    Args:
        repo (UserRepository): Репозиторий пользователей для работы с базой данных.
        payload (dict): Декодированный payload JWT-токена.

    Returns:
        UserModels: Объект пользователя из базы данных, соответствующий токену.

    Raises:
        HTTPException: Статус 404, если пользователь с указанным username не найден в базе данных.
    """
    username = payload.get("username")
    user = await repo.find_by_username(username)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


async def get_current_is_user(
    current_user: UserModels = Depends(get_current_auth_users)
) -> UserModels:
    """
    Проверяет, что текущий пользователь авторизован и имеет доступ.

    Используется как зависимость для защищённых эндпоинтов.

    Args:
        current_user (UserModels): Текущий аутентифицированный пользователь.

    Returns:
        UserModels: Подтверждённый пользователь.

    Raises:
        HTTPException: 403 — если у пользователя недостаточно прав.
    """

    if current_user:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')


async def validate_auth_user(
    repo: UserRepository,
    username: str = Form(),
    password: str = Form(),
):
    """
    Валидирует пользователя при аутентификации через форму.

    Функция проверяет наличие пользователя с указанным username в базе данных
    и корректность переданного пароля путём сравнения с хэшированным паролем.
    Для работы с базой используется репозиторий пользователей `repo`.

    Args:
        repo (UserRepository): Репозиторий пользователей для работы с базой данных.
        username (str): Имя пользователя, введённое в форме.
        password (str): Пароль пользователя, введённый в форме.

    Returns:
        UserModels: Объект пользователя из базы данных при успешной аутентификации.

    Raises:
        HTTPException: 401 — если пользователь с таким username не найден
        или пароль не совпадает с хэшированным в базе данных.
    """
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = await repo.find_by_username(username)
    if not user:
        raise unauth_exc

    if validate_password(
        password=password,
        hashed_password=user.password,
    ):
        return user
    else:
        raise unauth_exc



