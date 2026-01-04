from backend.app.database.models import UserModels
from backend.app.repositories.tasks import TaskRepository
from backend.app.schemas.task_schemas import TaskSchema


class CreateTaskUseCase:
    """
    Юзкейc для создания новой задачи для пользователя.

    Attributes:
        repo: Репозиторий задач, реализующий метод create_one_task.
    """

    def __init__(self, repo: TaskRepository):
        """
        Инициализация use-case с указанием репозитория.

        Args:
            repo: Экземпляр TaskRepository для работы с задачами.
        """
        self.repo = repo

    async def execute(self, credentials: TaskSchema, current_user: UserModels) -> dict:
        """
        Создаёт новую задачу для указанного пользователя.

        Args:
            credentials (TaskSchema): Данные задачи (title, description).
            current_user (UserModels): Пользователь, которому принадлежит задача.

        Returns:
            dict: Словарь с сообщением о результате выполнения.
        """
        await self.repo.create_one_task(credentials, current_user)
        return {'msg': "Задача успешно создана"}
