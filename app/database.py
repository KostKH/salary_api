from sqlalchemy import Column, Integer
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from .config import settings
from sqlalchemy.orm import mapped_column

class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = mapped_column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        await async_session.execute(text('PRAGMA foreign_keys = ON'))
        yield async_session