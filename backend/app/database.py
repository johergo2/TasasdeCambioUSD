import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL",
                         "postgresql://usuario_api:qLOEsZzJHzqjNBEQDuwEjGXL2dGU4Aq5@dpg-d4s5b77diees73dkljd0-a.ohio-postgres.render.com/db_api_usuarios")

if DATABASE_URL is None:
    raise ValueError("La variable de entorno DATABASE_URL no está definida")

# Ajuste necesario para asyncpg
DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
