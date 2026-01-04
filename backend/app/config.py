from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из .env или по умолчанию.

    Attributes:
        host (str): Хост базы данных.
        user (str): Имя пользователя для подключения к БД.
        password (str): Пароль пользователя для подключения к БД.
        db_name (str): Название базы данных.
        port (str): Порт подключения к БД.
        pg_url (str): Полный URL подключения к PostgreSQL.
        echo (bool): Включение логирования SQL-запросов (по умолчанию False).

        private_key_path (Path): Путь к приватному ключу для JWT.
        public_key_path (Path): Путь к публичному ключу для JWT.
        algorithm (str): Алгоритм для JWT (по умолчанию RS256).
        access_token_expire_minutes (int): Время жизни access token в минутах (по умолчанию 15).
    """

    # PostgreSQL / база данных
    host: str
    user: str
    password: str
    db_name: str
    port: str
    pg_url: str
    echo: bool = False

    # JWT / безопасность
    private_key_path: Path = Path(__file__).parent / "certs" / "jwt-private.pem"
    public_key_path: Path = Path(__file__).parent / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15

    class Config:
        """Настройки для работы с .env файлом."""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Экземпляр настроек, который импортируется по всему приложению
settings = Settings()
