from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tasks import Task
from app.repositories.repositoriy import TaskRepository
from app.schemas.shemas import TaskUpdate, TaskCreate


class TaskNotFoundError(Exception):
    """task does not exist"""


class TaskService:
    def __init__(self, session: AsyncSession, repository: TaskRepository):
        self.session = session
        self.repository = repository

    async def get_task(self, task_id: int):
        task = await self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()
        return task

    async def get_tasks(
            self,
            is_completed: bool | None = None,
            search: str | None = None,
            sort_by: str = "id",
            order: str = "desc",
            limit: int = 20,
            offset: int = 0) -> list[Task]:

        query = select(Task)

        if is_completed is not None:
            query = query.where(Task.is_completed == is_completed)

        if search:
            query = query.where(Task.title.ilike(f"%{search}%"))

        sort_columns = {
            "id": Task.id,
            "title": Task.title,
            "is_completed": Task.is_completed,
        }

        column = sort_columns[sort_by]

        if order == "desc":
            query = query.order_by(column.desc())

        else:
            query = query.order_by(column.asc())

        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return list(result.scalars().all())


    async def create_task(self, task_data: TaskCreate):
        try:
            task = await self.repository.create(task_data)
            await self.session.commit()
            return task
        except Exception:
            await self.session.rollback()
            raise


    async def update_task(self, task_id: int, task_data: TaskUpdate):
        try:
            task = await self.get_task(task_id)
            task = await self.repository.update(task, task_data)
            await self.session.commit()
            return task
        except Exception:
            await self.session.rollback()
            raise


    async def replace_task(
        self,
        task_id: int,
        data: TaskCreate,
):
        task = await self.get_task(task_id)
        return await self.repository.replace(task, data)
        await self.session.commit()
        return task

    async def delete_task(self, task_id: int) -> None:
        try:
            task = await self.get_task(task_id)
            await self.repository.delete(task)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise