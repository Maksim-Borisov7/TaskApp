from fastapi import APIRouter, Depends

from backend.app.database.models import UserModels
from backend.app.dependencies.auth import get_current_is_user
from backend.app.dependencies.use_cases import (
    get_list_tasks_use_case,
    get_create_task_use_case,
    get_change_task_state_use_case,
    get_delete_task_use_case
)
from backend.app.schemas.task_schemas import TaskSchema
from backend.app.use_case.create_task import CreateTaskUseCase
from backend.app.use_case.delete_task import DeleteTaskUseCase
from backend.app.use_case.get_list_tasks import GetListTasksUseCase
from backend.app.use_case.change_task_state import ChangeTaskStateUseCase

router = APIRouter(prefix='/tasks', tags=["tasks"])


@router.get("/get/", summary="Получение списка задач пользователя")
async def get_list_tasks(
    current_user: UserModels = Depends(get_current_is_user),
    use_case: GetListTasksUseCase = Depends(get_list_tasks_use_case),
):
    """
    Получает список всех задач текущего пользователя.

    Args:
        current_user (UserModels): Текущий аутентифицированный пользователь.
        use_case (GetListTasksUseCase): Use-case для получения списка задач.

    Returns:
        list: Список задач пользователя (TaskModels).
    """
    return await use_case.execute(current_user)


@router.post("/create/", summary="Создание новой задачи")
async def create_task(
    credentials: TaskSchema,
    use_case: CreateTaskUseCase = Depends(get_create_task_use_case),
    current_user: UserModels = Depends(get_current_is_user),
):
    """
    Создаёт новую задачу для текущего пользователя.

    Args:
        credentials (TaskSchema): Данные новой задачи (title, description).
        use_case (CreateTaskUseCase): Use-case для создания задачи.
        current_user (UserModels): Текущий аутентифицированный пользователь.

    Returns:
        dict: Сообщение об успешном создании задачи.
            Например: {'msg': "Задача успешно создана"}.
    """
    return await use_case.execute(credentials, current_user)


@router.put("/update/{task_id}", summary="Изменение статуса задачи")
async def change_task_state(
    task_id: int,
    use_case: ChangeTaskStateUseCase = Depends(get_change_task_state_use_case),
    current_user: UserModels = Depends(get_current_is_user),
):
    """
    Изменяет статус выполнения задачи (выполнена / не выполнена).

    Args:
        task_id (int): ID задачи для обновления.
        use_case (ChangeTaskStateUseCase): Use-case для изменения статуса задачи.
        current_user (UserModels): Текущий аутентифицированный пользователь.

    Returns:
        dict: Сообщение о новом статусе задачи.
            Например: {'msg': "Задача отмечена как 'выполнена'"}.
    """
    return await use_case.execute(task_id)


@router.delete("/delete/{task_id}", summary="Удаление задачи")
async def delete_task(
    task_id: int,
    use_case: DeleteTaskUseCase = Depends(get_delete_task_use_case),
    current_user: UserModels = Depends(get_current_is_user),
):
    """
    Удаляет задачу по её ID.

    Args:
        task_id (int): ID задачи для удаления.
        use_case (DeleteTaskUseCase): Use-case для удаления задачи.
        current_user (UserModels): Текущий аутентифицированный пользователь.

    Returns:
        dict: Сообщение об успешном удалении задачи.
            Например: {'msg': "Задача успешно удалена"}.
    """
    return await use_case.execute(task_id)
