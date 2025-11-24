from __future__ import annotations
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Book, BookStatus
from .schemas import BookCreate, BookUpdate


async def create_book(db: AsyncSession, data: BookCreate) -> Book:
	book = Book(**data.model_dump())
	db.add(book)
	await db.commit()
	await db.refresh(book)
	return book


async def get_book(db: AsyncSession, book_id: int) -> Book | None:
	res = await db.execute(select(Book).where(Book.id == book_id))
	return res.scalar_one_or_none()


async def list_books(db: AsyncSession, *, q: str | None, status: BookStatus | None, limit: int, offset: int):
	query = select(Book)
	if q:
		like = f"%{q}%"
		query = query.where((Book.title.ilike(like)) | (Book.author.ilike(like)))
	if status:
		query = query.where(Book.status == status)
	total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar_one()
	query = query.order_by(Book.created_at.desc()).limit(limit).offset(offset)
	items = (await db.execute(query)).scalars().all()
	return items, total


async def update_book(db: AsyncSession, book: Book, data: BookUpdate) -> Book:
	for k, v in data.model_dump(exclude_unset=True).items():
		setattr(book, k, v)
	await db.commit()
	await db.refresh(book)
	return book


async def delete_book(db: AsyncSession, book: Book) -> None:
	await db.delete(book)
	await db.commit()