from datetime import datetime, timezone, timedelta
from backend.app.config import settings
from jose import jwt


def encode_jwt(
        payload: dict,
        algorithm=settings.algorithm,
        expire_minutes: int = settings.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    """
    Кодирует JWT-токен доступа.

    Создаёт JSON Web Token (JWT) на основе переданного payload и
    криптографических параметров. В токен автоматически добавляются
    стандартные JWT-поля:
    - exp — время истечения токена
    - iat — время создания токена

    Время жизни токена можно задать двумя способами:
    - через количество минут (`expire_minutes`);
    - через объект `timedelta` (`expire_timedelta`), который имеет приоритет.

    Args:
        payload (dict): Данные (claims), которые будут включены в токен.
        private_key (str): Приватный ключ для подписи токена.
        algorithm (str): Алгоритм подписи JWT.
        expire_minutes (int): Время жизни токена в минутах.
        expire_timedelta (timedelta | None): Пользовательский интервал
            времени жизни токена. Если указан, `expire_minutes` игнорируется.

    Returns:
        str: Сформированный JWT-токен.
    """
    private_key = settings.private_key_path.read_text()

    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        algorithm=settings.algorithm,
) -> dict:
    """
    Декодирует и валидирует JWT-токен.

    Проверяет подпись токена и извлекает payload с использованием
    публичного ключа и указанного алгоритма. Также автоматически
    проверяются стандартные JWT-поля.

    Args:
        token (str | bytes): JWT-токен для декодирования.
        public_key (str): Публичный ключ для проверки подписи токена.
        algorithm (str): Алгоритм проверки подписи JWT.

    Returns:
        dict: Декодированное содержимое JWT (payload).
    """
    public_key = settings.public_key_path.read_text()
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
