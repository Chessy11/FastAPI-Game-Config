from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username="postgres",
    password="potoli11",
    host="localhost",
    port=5432,
    database="gamedb"
)


engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
