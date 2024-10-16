import asyncpg
from sqlalchemy.ext .asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from sqlalchemy.dialects import registry
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_async_engine(f"postgresql+asyncpg://{os.getenv('DB_LOGIN')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/postgres?role=egor",
                             )
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
metadata = MetaData(schema='fastapi_ecommerce')


class Base(DeclarativeBase):
    metadata = metadata