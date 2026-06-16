import asyncio
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
DATABASE_URL = f"postgresql+asyncpg://"  # Ваши данные сюда)))
SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "").replace("postgresql+asyncpg", "postgresql")


async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass



