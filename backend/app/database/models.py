from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM-моделей SQLAlchemy.

    Используется как корневой класс декларативных моделей.
    Все модели приложения должны наследоваться от данного класса.
    """
    pass


class TaskModels(Base):
    """
    ORM-модель задачи пользователя.

    Представляет сущность задачи, связанной с конкретным пользователем.
    Хранит информацию о названии задачи, описании, статусе выполнения
    и времени создания.

    Attributes:
        task_id (int): Уникальный идентификатор задачи.
        title (str): Название задачи.
        description (str | None): Описание задачи (может быть пустым).
        is_done (bool): Статус выполнения задачи.
        created_at (datetime): Дата и время создания задачи.
        user_id (int): Идентификатор пользователя-владельца задачи.
        user (UserModels): Связанный пользователь.
    """

    __tablename__ = 'tasks'

    task_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_done: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModels"] = relationship(
        "UserModels",
        back_populates="tasks",
    )


class UserModels(Base):
    """
    ORM-модель пользователя.

    Описывает сущность пользователя системы. Пользователь может
    иметь несколько задач, связанных с ним.

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        username (str): Уникальное имя пользователя.
        password (bytes): Хэш пароля пользователя.
        email (str): Электронная почта пользователя.
        tasks (list[TaskModels]): Список задач пользователя.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    email: Mapped[str] = mapped_column(unique=True)

    tasks: Mapped[list["TaskModels"]] = relationship(
        "TaskModels",
        back_populates="user",
    )
