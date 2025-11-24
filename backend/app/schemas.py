from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from .models import BookStatus


class BookBase(BaseModel):
	title: str = Field(..., max_length=255)
	author: str = ""
	pages: Optional[int] = None
	year: Optional[int] = None
	status: BookStatus = BookStatus.PLANNED
	started_at: Optional[date] = None
	finished_at: Optional[date] = None
	rating: Optional[int] = Field(default=None, ge=1, le=5)
	notes: str = ""


class BookCreate(BookBase):
	pass


class BookUpdate(BaseModel):
	title: Optional[str] = Field(default=None, max_length=255)
	author: Optional[str] = None
	pages: Optional[int] = None
	year: Optional[int] = None
	status: Optional[BookStatus] = None
	started_at: Optional[date] = None
	finished_at: Optional[date] = None
	rating: Optional[int] = Field(default=None, ge=1, le=5)
	notes: Optional[str] = None


class BookOut(BookBase):
	id: int
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None


class Config:
	from_attributes = True


class Page(BaseModel):
	items: list[BookOut]
	total: int
	limit: int
	offset: int