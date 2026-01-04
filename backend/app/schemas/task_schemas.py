from typing import Optional
from pydantic import BaseModel, Field


class TaskSchema(BaseModel):
    """
    Схема для создания или передачи данных задачи.

    Attributes:
        title (str): Заголовок задачи. Обязательное поле.
        description (Optional[str]): Описание задачи. Необязательное поле.
    """

    title: str = Field(..., min_length=1, max_length=255, description="Заголовок задачи (обязательное)")
    description: Optional[str] = Field(None, max_length=1024, description="Описание задачи (необязательное)")
