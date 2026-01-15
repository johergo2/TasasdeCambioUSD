import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("postgresql://usuario_api:qLOEsZzJHzqjNBEQDuwEjGXL2dGU4Aq5@dpg-d4s5b77diees73dkljd0-a.ohio-postgres.render.com/db_api_usuarios")

engine = create_async_engine(
    DATABASE_URL.replace("postgres://", "postgresql+asyncpg://"),
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
