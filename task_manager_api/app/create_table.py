
import asyncio

from app.core.database import engine
from app.models.tasks import Task


async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Task.metadata.create_all)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())
