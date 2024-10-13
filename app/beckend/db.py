from sqlalchemy.ext .asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_async_engine(f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/postgres")
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
metadata = MetaData(schema='fastapi_ecommerce')


class Base(DeclarativeBase):
    metadata = metadata