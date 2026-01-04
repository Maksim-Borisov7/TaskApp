from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.models import UserModels


class UserRepository:
    """
    Репозиторий для работы с пользователями (UserModels).

    Инкапсулирует все операции CRUD по пользователям.

    Attributes:
        model: Ссылка на ORM-модель UserModels.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
    """

    model = UserModels

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД.
        """
        self.session = session

    async def find_by_username_or_email(self, username: str, email: str) -> UserModels | None:
        """
        Находит пользователя по username или email.

        Args:
            username (str): Имя пользователя.
            email (str): Email пользователя.

        Returns:
            UserModels | None: Экземпляр пользователя, если найден, иначе None.
        """
        query = select(self.model).where(
            (self.model.username == username) |
            (self.model.email == email)
        )
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def find_by_username(self, username: str) -> UserModels | None:
        """
        Находит пользователя по username.

        Args:
            username (str): Имя пользователя.

        Returns:
            UserModels | None: Экземпляр пользователя, если найден, иначе None.
        """
        query = select(self.model).where(self.model.username == username)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def add_user(self, **kwargs) -> None:
        """
        Создаёт нового пользователя и сохраняет его в базе данных.

        Args:
            **kwargs: Поля пользователя, например username, email, password.

        Returns:
            None
        """
        user = self.model(**kwargs)
        self.session.add(user)
        await self.session.commit()
