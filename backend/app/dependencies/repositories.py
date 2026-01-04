from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.database import database
from backend.app.repositories.tasks import TaskRepository
from backend.app.repositories.users import UserRepository


def get_user_repo(
        session: AsyncSession = Depends(database.get_session),
) -> UserRepository:
    """
    Создаёт и возвращает экземпляр UserRepository с переданной сессией БД.

    Используется как зависимость FastAPI (`Depends`) для эндпоинтов,
    где нужен доступ к репозиторию пользователей.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy, предоставляемая через Depends.

    Returns:
        UserRepository: Экземпляр репозитория пользователей, привязанный к сессии.
    """
    return UserRepository(session)


def get_task_repo(
        session: AsyncSession = Depends(database.get_session),
) -> TaskRepository:
    """
    Создаёт и возвращает экземпляр TaskRepository с переданной сессией БД.

    Используется как зависимость FastAPI (`Depends`) для эндпоинтов,
    где нужен доступ к репозиторию задач.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy, предоставляемая через Depends.

    Returns:
        TaskRepository: Экземпляр репозитория задач, привязанный к сессии.
    """
    return TaskRepository(session)

