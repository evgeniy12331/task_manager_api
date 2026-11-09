from sqlalchemy import URL
from sqlalchemy.ext.asyncio import(
AsyncSession,
async_sessionmaker,
create_async_engine
)
from app.core.config import settings

DATABASE = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)
engine = create_async_engine(DATABASE,echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Этот файл отвечает за создание подключения к PostgreSQL, управление асинхронными сессиями и передачу сессии в другие части приложения.