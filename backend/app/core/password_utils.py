import bcrypt


def hash_password(password: str) -> bytes:
    """
    Хеширование пароля с солью.
    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    """
    Проверка соответствия пароля хешу.
    """
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
