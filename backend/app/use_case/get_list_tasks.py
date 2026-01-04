from typing import Sequence
from backend.app.database.models import TaskModels, UserModels
from backend.app.repositories.tasks import TaskRepository


class GetListTasksUseCase:
    """
    Юзкейc для получения списка задач текущего пользователя.

    Attributes:
        repo (TaskRepository): Репозиторий задач для работы с БД.
    """

    def __init__(self, repo: TaskRepository):
        """
        Инициализация use-case с указанием репозитория.

        Args:
            repo (TaskRepository): Репозиторий задач.
        """
        self.repo = repo

    async def execute(self, current_user: UserModels) -> Sequence[TaskModels]:
        """
        Получает все задачи, принадлежащие текущему пользователю.

        Args:
            current_user (UserModels): Пользователь, для которого возвращаем задачи.

        Returns:
            Sequence[TaskModels]: Список объектов задач.
        """
        return await self.repo.get_tasks(current_user)
