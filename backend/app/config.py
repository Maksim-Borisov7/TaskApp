import subprocess

from pydantic_settings import BaseSettings
from pathlib import Path


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

        generate_keys_if_not_exist:
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

    def generate_keys_if_not_exist(self):
        """Генерирует приватный и публичный ключ"""
        certs_dir = self.private_key_path.parent
        private_key_path = self.private_key_path
        public_key_path = self.public_key_path

        if private_key_path.exists() and public_key_path.exists():
            return

        print("Ключи JWT не найдены → генерируем новые для разработки...")

        certs_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Генерация приватного ключа
            subprocess.run(
                ["openssl", "genrsa", "-out", str(private_key_path), "2048"],
                check=True,
                capture_output=True,
                text=True
            )

            # Извлечение публичного ключа
            subprocess.run(
                ["openssl", "rsa", "-in", str(private_key_path), "-pubout", "-out", str(public_key_path)],
                check=True,
                capture_output=True,
                text=True
            )

            print(f"Ключи сгенерированы:\n  {private_key_path}\n  {public_key_path}")
        except subprocess.CalledProcessError as e:
            print("Ошибка генерации ключей:", e.stderr)
            raise RuntimeError("Не удалось сгенерировать JWT-ключи")


settings = Settings()
