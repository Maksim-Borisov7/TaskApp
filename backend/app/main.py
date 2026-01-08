from contextlib import asynccontextmanager

from backend.app.config import settings
from backend.app.database.database import database
from backend.app.logs.logger import logger
from fastapi import FastAPI
from backend.app.api.auth import router as router_auth
from backend.app.api.tasks import router as router_tasks
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла FastAPI.

    Используется для:
    - Логирования запуска и завершения сервера
    - Создания таблиц в базе данных при старте

    Args:
        app (FastAPI): Экземпляр FastAPI приложения.
    """
    try:
        logger.info("Запуск сервера")
        settings.generate_keys_if_not_exist()
        await database.create_table()
        logger.info("Таблицы созданы")
        yield
        logger.info("Выключение сервера")
    except ConnectionRefusedError as e:
        logger.warning(f"Не удалось подключиться к БД: {e}")


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_tasks)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
