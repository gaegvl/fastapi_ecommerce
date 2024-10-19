import asyncpg
from sqlalchemy.ext .asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
import os
from dotenv import load_dotenv
load_dotenv()


URI = f"postgresql+asyncpg://{os.getenv('DB_LOGIN')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/postgres"


class Database:
    def __init__(self):
        self.engine = create_async_engine(URI)
        self.session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False, autoflush=False, autocommit=False)

    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session
            await session.close()


metadata = MetaData(schema='fastapi_ecommerce')


class Base(DeclarativeBase):
    metadata = metadata