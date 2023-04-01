from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os


DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv('DB_USER', 'conf_db_user'),
    password=os.getenv('DB_PASSWORD', 'AVNS_C3kJJkHO2hH0gGwtaco'),
    host=os.getenv('DB_HOST', 'dev-db-all-services-do-user-6051737-0.b.db.ondigitalocean.com'),
    port=os.getenv('DB_PORT', '25060'),
    database=os.getenv('DB_NAME', 'conf_db')
)


engine = create_async_engine(DATABASE_URL, connect_args={"ssl": "require"})
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
