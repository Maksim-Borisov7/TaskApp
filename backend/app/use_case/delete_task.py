from backend.app.repositories.tasks import TaskRepository


class DeleteTaskUseCase:
    """
    Юзкейc для удаления задачи по её ID.

    Attributes:
        repo: Репозиторий задач, реализующий метод delete_task_by_id.
    """

    def __init__(self, repo: TaskRepository):
        """
        Инициализация use-case с указанием репозитория.

        Args:
            repo: Экземпляр TaskRepository для работы с задачами.
        """
        self.repo = repo

    async def execute(self, task_id: int) -> dict:
        """
        Удаляет задачу с указанным ID.

        Args:
            task_id (int): ID задачи для удаления.

        Returns:
            dict: Словарь с сообщением о результате удаления.
        """
        await self.repo.delete_task_by_id(task_id)
        return {'msg': "Задача успешно удалена"}
