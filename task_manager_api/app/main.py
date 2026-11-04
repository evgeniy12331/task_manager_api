from fastapi import FastAPI
from app.routers.tasks import router as tasks_router
app = FastAPI(title='task manager api',
              description='api for tasks',
              version='1.0.0')

app.include_router(tasks_router)


