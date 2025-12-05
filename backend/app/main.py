from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Response
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from .database import init_db, get_session
from .models import BookStatus, Book
from .schemas import BookCreate, BookUpdate, BookOut, Page
from .crud import create_book, get_book, list_books, update_book, delete_book
from .deps import pagination
from .utils_csv import books_to_csv


app = FastAPI(title="Libros API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Backend funcionando!"}


@app.on_event("startup")
async def on_startup():
    # Crea las tablas en la BD si no existen (usa tu init_db)
    await init_db()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/books", response_model=BookOut, status_code=201)
async def create_book_ep(
    payload: BookCreate,
    db: AsyncSession = Depends(get_session),
):
    book = await create_book(db, payload)
    return book


@app.get("/books", response_model=Page)
async def list_books_ep(
    q: Optional[str] = None,
    status: Optional[BookStatus] = None,
    page=Depends(pagination),
    db: AsyncSession = Depends(get_session),
):
    items, total = await list_books(
        db,
        q=q,
        status=status,
        limit=page["limit"],
        offset=page["offset"],
    )
    return {
        "items": items,
        "total": total,
        "limit": page["limit"],
        "offset": page["offset"],
        
    }


@app.get("/books/export.csv")
async def export_books_csv(db: AsyncSession = Depends(get_session)):
    items, _ = await list_books(
        db,
        q=None,
        status=None,
        limit=10000,
        offset=0,
    )

    csv_content = books_to_csv(items)

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="books_export.csv"'
        },
    )





@app.get("/books/{book_id}", response_model=BookOut)
async def get_book_ep(
    book_id: int,
    db: AsyncSession = Depends(get_session),
):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.patch("/books/{book_id}", response_model=BookOut)
async def update_book_ep(
    book_id: int,
    payload: BookUpdate,
    db: AsyncSession = Depends(get_session),
):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return await update_book(db, book, payload)


@app.delete("/books/{book_id}", status_code=204)
async def delete_book_ep(
    book_id: int,
    db: AsyncSession = Depends(get_session),
):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await delete_book(db, book)
    return Response(status_code=204)


@app.patch("/books/{book_id}/status", response_model=BookOut)
async def set_status_ep(
    book_id: int,
    status: BookStatus,
    db: AsyncSession = Depends(get_session),
):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Reutilizamos el mismo update con un BookUpdate parcial
    return await update_book(db, book, BookUpdate(status=status))
