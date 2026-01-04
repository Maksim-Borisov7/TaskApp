from fastapi import HTTPException, status

from backend.app.core.password_utils import hash_password
from backend.app.repositories.users import UserRepository
from backend.app.schemas.user_schemas import UserRegistrationSchema


class CreateUserUseCase:
    """
    Юзкейc для регистрации нового пользователя.

    Attributes:
        repo (UserRepository): Репозиторий пользователей для работы с БД.
    """

    def __init__(self, repo: UserRepository):
        """
        Инициализация use-case с указанием репозитория.

        Args:
            repo (UserRepository): Репозиторий пользователей.
        """
        self.repo = repo

    async def execute(self, data: UserRegistrationSchema) -> dict:
        """
        Создаёт нового пользователя, если username и email ещё не заняты.

        Args:
            data (UserRegistrationSchema): Данные нового пользователя
                                           (username, email, password).

        Returns:
            dict: Словарь с сообщением об успешной регистрации.

        Raises:
            HTTPException: Если пользователь с таким username или email уже существует.
        """

        existing_user = await self.repo.find_by_username_or_email(data.username, data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь уже зарегистрирован"
            )

        user_data = data.model_dump()
        user_data["password"] = hash_password(data.password)

        await self.repo.add_user(**user_data)
        return {"msg": "Пользователь успешно зарегистрирован"}
