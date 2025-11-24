from __future__ import annotations
import os
from fastapi import Query


DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", 50))
MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", 200))


def pagination(
	limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
	offset: int = Query(0, ge=0),
):
	return {"limit": limit, "offset": offset}