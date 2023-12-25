from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'postgres'),
    host=os.getenv('DB_HOST', 'db'),
    port=os.getenv('DB_PORT', '5432'),
    database=os.getenv('DB_NAME', 'gamedb'),
)

# DATABASE_URL = "postgresql+asyncpg://postgres:potoli11@localhost:5432/gamedb"


engine = create_async_engine(str(DATABASE_URL), connect_args={"ssl": None})

SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
