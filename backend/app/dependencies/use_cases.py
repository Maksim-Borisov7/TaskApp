from fastapi import Depends

from backend.app.dependencies.repositories import get_user_repo, get_task_repo
from backend.app.repositories.tasks import TaskRepository
from backend.app.repositories.users import UserRepository
from backend.app.use_case.auth_user import AuthUserUseCase
from backend.app.use_case.create_task import CreateTaskUseCase
from backend.app.use_case.create_user import CreateUserUseCase
from backend.app.use_case.get_list_tasks import GetListTasksUseCase
from backend.app.use_case.change_task_state import ChangeTaskStateUseCase
from backend.app.use_case.delete_task import DeleteTaskUseCase


def get_create_user_use_case(repo: UserRepository = Depends(get_user_repo)) -> CreateUserUseCase:
    """
    Создаёт и возвращает экземпляр use-case для регистрации пользователя.

    Args:
        repo (UserRepository): Репозиторий пользователей, предоставленный через Depends.

    Returns:
        CreateUserUseCase: Use-case для создания нового пользователя.
    """
    return CreateUserUseCase(repo)


def get_auth_user_use_case(repo: UserRepository = Depends(get_user_repo)) -> AuthUserUseCase:
    """
    Создаёт и возвращает экземпляр use-case для аутентификации пользователя.

    Args:
        repo (UserRepository): Репозиторий пользователей, предоставленный через Depends.

    Returns:
        AuthUserUseCase: Use-case для аутентификации пользователя.
    """
    return AuthUserUseCase(repo)


def get_list_tasks_use_case(repo: TaskRepository = Depends(get_task_repo)):
    """
    Создаёт и возвращает экземпляр use-case для получения списка задач.

    Args:
        repo (TaskRepository): Репозиторий задач, предоставленный через Depends.

    Returns:
        GetListTasksUseCase: Use-case для получения списка задач пользователя.
    """
    return GetListTasksUseCase(repo)


def get_create_task_use_case(repo: TaskRepository = Depends(get_task_repo)):
    """
    Создаёт и возвращает экземпляр use-case для создания новой задачи.

    Args:
        repo (TaskRepository): Репозиторий задач, предоставленный через Depends.

    Returns:
        CreateTaskUseCase: Use-case для создания новой задачи.
    """
    return CreateTaskUseCase(repo)


def get_change_task_state_use_case(repo: TaskRepository = Depends(get_task_repo)):
    """
    Создаёт и возвращает экземпляр use-case для изменения статуса задачи.

    Args:
        repo (TaskRepository): Репозиторий задач, предоставленный через Depends.

    Returns:
        ChangeTaskStateUseCase: Use-case для изменения состояния задачи.
    """
    return ChangeTaskStateUseCase(repo)


def get_delete_task_use_case(repo: TaskRepository = Depends(get_task_repo)):
    """
    Создаёт и возвращает экземпляр use-case для удаления задачи.

    Args:
        repo (TaskRepository): Репозиторий задач, предоставленный через Depends.

    Returns:
        DeleteTaskUseCase: Use-case для удаления задачи.
    """
    return DeleteTaskUseCase(repo)
