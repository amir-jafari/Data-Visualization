"""Shared dependencies -- the things more than one route needs.

Every one of these is a plain function. That is what makes them replaceable in
tests (see tests/test_api.py) and what keeps the routers readable.
"""

from hmac import compare_digest

import pandas as pd
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import APIKeyHeader

from . import store
from .config import Settings, get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(
    key: str | None = Depends(api_key_header),
    settings: Settings = Depends(get_settings),
) -> str:
    """Guard the write-ish and expensive routes."""
    if key is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing X-API-Key header")
    if not compare_digest(key, settings.api_key):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API key")
    return key


class Pagination:
    """limit/offset, bounded by settings so a caller cannot ask for everything."""

    def __init__(
        self,
        limit: int | None = Query(None, ge=1, description="Rows per page"),
        offset: int = Query(0, ge=0),
        settings: Settings = Depends(get_settings),
    ):
        self.limit = min(limit or settings.page_size, settings.max_page_size)
        self.offset = offset


def get_dataset(name: str) -> pd.DataFrame:
    """Resolve a dataset name from the path, or 404.

    Written once here instead of at the top of every route that needs it.
    """
    frame = store.load(name)
    if frame is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"No dataset called {name!r}. Available: {', '.join(store.names())}",
        )
    return frame
