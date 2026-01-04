from typing import Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.models import TaskModels, UserModels
from backend.app.schemas.task_schemas import TaskSchema


class TaskRepository:
    """
    Репозиторий для работы с задачами (TaskModels).

    Инкапсулирует все операции с базой данных по CRUD задач.

    Attributes:
    model: Ссылка на ORM-модель TaskModels.
    session (AsyncSession): Асинхронная сессия для работы с базой данных.
    """

    model = TaskModels

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД.
        """
        self.session = session

    async def get_tasks(self, current_user: UserModels) -> Sequence[TaskModels]:
        """
        Получает список всех задач текущего пользователя.

        Args:
            current_user (UserModels): Текущий пользователь, для которого ищем задачи.

        Returns:
            Sequence[TaskModels]: Список задач пользователя.
        """
        query = select(self.model).where(self.model.user_id == current_user.id)
        res = await self.session.execute(query)
        tasks = res.scalars().all()
        return tasks

    async def get_task_by_id(self, task_id: int) -> TaskModels | None:
        """
        Получает задачу по её ID.

        Args:
            task_id (int): Идентификатор задачи.

        Returns:
            TaskModels | None: Задача с указанным ID или None, если не найдена.
        """
        query = select(self.model).where(self.model.task_id == task_id)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def create_one_task(self, credentials: TaskSchema, current_user: UserModels):
        """
        Создаёт новую задачу для текущего пользователя.

        Args:
            credentials: Объект с данными новой задачи (title, description).
            current_user (UserModels): Пользователь, которому принадлежит задача.

        """
        query = self.model(
            title=credentials.title,
            description=credentials.description,
            user_id=current_user.id
        )
        self.session.add(query)
        await self.session.commit()

    async def change_task(self, task_id: int, value: bool):
        """
        Изменяет состояние выполнения задачи.

        Args:
            task_id (int): Идентификатор задачи.
            value (bool): Новое состояние (True — выполнено, False — не выполнено).

        """
        query = (
            update(self.model)
            .where(self.model.task_id == task_id)
            .values(is_done=value)
        )
        await self.session.execute(query)
        await self.session.commit()

    async def delete_task_by_id(self, task_id: int):
        """
        Удаляет задачу по её ID.

        Args:
            task_id (int): Идентификатор задачи.

        """
        await self.session.execute(delete(self.model).where(self.model.task_id == task_id))
        await self.session.commit()
