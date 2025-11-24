from __future__ import annotations
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .models import Base


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./libros.db")


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False, autocommit=False, class_=AsyncSession)


async def init_db():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
	async with AsyncSessionLocal() as session:
		yield session