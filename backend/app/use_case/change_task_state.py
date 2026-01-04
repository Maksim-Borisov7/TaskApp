from backend.app.repositories.tasks import TaskRepository


class ChangeTaskStateUseCase:
    """
    Юзкейc для изменения состояния задачи (выполнена / не выполнена).

    Attributes:
        repo: Репозиторий задач, реализующий методы get_task_by_id и change_task.
    """

    def __init__(self, repo: TaskRepository):
        """
        Инициализация use-case с указанием репозитория.

        Args:
            repo: Экземпляр TaskRepository для работы с задачами.
        """
        self.repo = repo

    async def execute(self, task_id: int) -> dict | None:
        """
        Переключает состояние задачи с выполненной на невыполненную или наоборот.

        Args:
            task_id (int): ID задачи для изменения состояния.

        Returns:
            dict | None: Словарь с сообщением о новом состоянии задачи, либо None,
                         если задача с указанным ID не найдена.
        """
        task = await self.repo.get_task_by_id(task_id)
        if task is None:
            return None

        if task.is_done:
            await self.repo.change_task(task_id, value=False)
            return {'msg': "Задача отмечена как 'не выполнена'"}

        await self.repo.change_task(task_id, value=True)
        return {'msg': "Задача отмечена как 'выполнена'"}
