import csv
from io import StringIO
from typing import List

from .models import BookStatus
from .schemas import BookOut


def orm_to_schema(book) -> BookOut:
    """
    Convierte un objeto ORM (Book) a un schema BookOut.
    Funciona sin importar si book ya es un BookOut o un ORM.
    """
    if isinstance(book, BookOut):
        return book

    # Convertimos manualmente del ORM a BookOut
    return BookOut(
        id=book.id,
        title=book.title,
        author=book.author,
        pages=book.pages,
        year=book.year,
        status=book.status if isinstance(book.status, BookStatus) else BookStatus(book.status),
        rating=book.rating,
        notes=book.notes,
        started_at=book.started_at,
        finished_at=book.finished_at,
        created_at=book.created_at,
        updated_at=book.updated_at,
    )


def books_to_csv(books: List) -> str:
    """
    Convierte una lista de libros (ORM o BookOut) a un string CSV.
    """
    output = StringIO()
    writer = csv.writer(output)

    # Encabezados del CSV
    writer.writerow([
        "id", "title", "author", "pages", "year",
        "status", "rating", "notes",
        "started_at", "finished_at",
        "created_at", "updated_at"
    ])

    # Procesar todos los libros
    for b in books:
        b = orm_to_schema(b)

        writer.writerow([
            b.id,
            b.title,
            b.author,
            b.pages or "",
            b.year or "",
            b.status.value,
            b.rating or "",
            b.notes or "",
            b.started_at.isoformat() if b.started_at else "",
            b.finished_at.isoformat() if b.finished_at else "",
            b.created_at.isoformat() if b.created_at else "",
            b.updated_at.isoformat() if b.updated_at else "",
        ])

    return output.getvalue()
