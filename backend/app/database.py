from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .models import Base  # Tu DeclarativeBase de models.py

load_dotenv()

# 👇 Usamos el dialecto ASÍNCRONO: mysql+aiomysql
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=False,   # pon True si quieres ver las queries en consola
    future=True,
)

# Session factory asíncrona
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """
    Crea las tablas en la base de datos si no existen.
    Se llama en el evento de startup de FastAPI.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """
    Dependencia para inyectar AsyncSession en los endpoints.
    """
    async with SessionLocal() as session:
        yield session
