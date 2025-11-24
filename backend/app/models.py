from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Enum, Text, DateTime, func
import enum
from datetime import date, datetime


class Base(DeclarativeBase):
	pass


class BookStatus(str, enum.Enum):
	PLANNED = "PLANNED"  # lista de espera
	READING = "READING"  # leyendo
	READ = "READ"  # leído


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    author: Mapped[str] = mapped_column(String(255), default="")
    pages: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[BookStatus] = mapped_column(
        Enum(BookStatus),
        default=BookStatus.PLANNED,
        index=True
    )
    started_at: Mapped[date | None] = mapped_column(nullable=True)
    finished_at: Mapped[date | None] = mapped_column(nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1..5 opcional
    notes: Mapped[str] = mapped_column(Text, default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
