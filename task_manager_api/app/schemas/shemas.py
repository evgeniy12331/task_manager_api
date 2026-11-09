from typing import Literal

from pydantic import (
BaseModel,
Field,
ConfigDict
)

TaskStatus = Literal['todo', 'in_progress', 'done']

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    priority: int = Field(default=3, ge=1, le=5)
    status: TaskStatus = 'todo'

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    priority: int | None = Field(default=None, ge=1, le=5)
    status: TaskStatus | None = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    priority: int
    status: TaskStatus

#     отвечает за проверку входящих данных от пользователя и формирование ответа API.
