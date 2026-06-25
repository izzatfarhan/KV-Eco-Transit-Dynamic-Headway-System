import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Defaulting to an async driver string for postgresql
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/kv_transit"
)

# Initialize SQLAlchemy Async Engine
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

# Create a configured async "SessionFactory"
SessionFactory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncSession:
    """
    Dependency function to yield an async database session.
    """
    async with SessionFactory() as session:
        yield session
