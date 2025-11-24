from __future__ import annotations
import csv
from io import StringIO
from typing import Iterable
from .models import Book


CSV_FIELDS = ["id", "title", "author", "pages", "year", "status", "started_at", "finished_at", "rating", "notes"]


def books_to_csv(books: Iterable[Book]) -> str:
	buf = StringIO()
	writer = csv.DictWriter(buf, fieldnames=CSV_FIELDS)
	writer.writeheader()
	for b in books:
		writer.writerow(
			{
				"id": b.id,
				"title": b.title,
				"author": b.author,
				"pages": b.pages,
				"year": b.year,
				"status": b.status.value,
				"started_at": b.started_at or "",
				"finished_at": b.finished_at or "",
				"rating": b.rating or "",
				"notes": b.notes or "",
			}
		)
	return buf.getvalue()