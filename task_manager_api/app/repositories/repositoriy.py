from app.models.tasks import Task
from app.schemas.shemas import TaskCreate, TaskUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, task_id: int):
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.session.execute(select(Task).order_by(Task.id))
        return list(result.scalars().all())

    async def create(self, task_data: TaskCreate):
        task = Task(**task_data.model_dump())
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task

    async def update(self,task: Task, task_data: TaskUpdate):
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        await self.session.flush()
        await self.session.refresh(task)
        return task

    async def replace(
            self,
            task: Task,
            data: TaskCreate,
    ) -> Task:
        for field, value in data.model_dump().items():
            setattr(task, field, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task: Task):
        await self.session.commit()
        await self.session.flush()
