from typing import Annotated, Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.repositoriy import TaskRepository
from app.schemas.shemas import TaskCreate, TaskUpdate, TaskResponse
from app.service.task_service import TaskService, TaskNotFoundError


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


async def get_task_service(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> TaskService:
    repository = TaskRepository(session)
    return TaskService(session, repository)


TaskServiceDep = Annotated[
    TaskService,
    Depends(get_task_service),
]


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskCreate,
    service: TaskServiceDep,
):
    return await service.create_task(data)


@router.get(
    "/",
    response_model=list[TaskResponse],
)
async def get_tasks(
    service: TaskServiceDep,
    is_completed: bool | None = None,
    search: Annotated[
        str | None,
        Query(min_length=1, max_length=200),
    ] = None,
    sort_by: Literal[
        "id",
        "title",
        "is_completed",
    ] = "id",
    order: Literal["asc", "desc"] = "desc",
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return await service.get_tasks(
        is_completed=is_completed,
        search=search,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    service: TaskServiceDep,
):
    try:
        return await service.get_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        ) from exc


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
async def update(
    task_id: int,
    data: TaskUpdate,
    service: TaskServiceDep,
):
    try:
        return await service.update_task(task_id, data)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        ) from exc


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
async def replace(
    task_id: int,
    data: TaskCreate,
    service: TaskServiceDep,
):
    try:
        return await service.replace_task(task_id, data)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        ) from exc


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    service: TaskServiceDep,
):
    try:
        await service.delete_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        ) from exc

    return None
