"""Reading data: list it, page through it, filter it, summarise it, export it."""

import csv
import io

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from .. import store
from ..deps import Pagination, get_dataset
from ..schemas import ColumnSummary, DatasetInfo, DatasetSummary, Page

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("", response_model=list[DatasetInfo])
def list_datasets():
    """The catalogue. Start here to find out what the other routes accept."""
    infos = []
    for name in store.names():
        frame = store.load(name)
        if frame is None:
            continue
        infos.append(DatasetInfo(
            name=name,
            rows=len(frame),
            columns=list(frame.columns),
            source=store.source_of(name),
        ))
    return infos


@router.get("/{name}", response_model=Page)
def read_dataset(
    name: str,
    frame: pd.DataFrame = Depends(get_dataset),
    page: Pagination = Depends(),
    column: str | None = Query(None, description="Column to filter on"),
    equals: str | None = Query(None, description="Keep rows where column == this"),
    sort_by: str | None = Query(None),
    descending: bool = False,
):
    """One page of rows, optionally filtered and sorted.

    Note the shape of the reply: the rows *and* the total. Without the total a
    client cannot draw a pager or know when to stop.
    """
    if column is not None:
        if column not in frame.columns:
            raise HTTPException(422, f"No column {column!r} in {name!r}")
        if equals is not None:
            # Compare as text so one query parameter works for every dtype.
            frame = frame[frame[column].astype(str) == equals]

    if sort_by is not None:
        if sort_by not in frame.columns:
            raise HTTPException(422, f"No column {sort_by!r} in {name!r}")
        frame = frame.sort_values(sort_by, ascending=not descending)

    total = len(frame)
    window = frame.iloc[page.offset:page.offset + page.limit]

    return Page(
        dataset=name,
        total=total,
        limit=page.limit,
        offset=page.offset,
        returned=len(window),
        # NaN is not valid JSON; None is.
        rows=window.where(pd.notnull(window), None).to_dict(orient="records"),
    )


@router.get("/{name}/summary", response_model=DatasetSummary)
def summarise(name: str, frame: pd.DataFrame = Depends(get_dataset)):
    """Per-column statistics -- the API version of df.describe()."""
    columns = []
    for col in frame.columns:
        series = frame[col]
        summary = ColumnSummary(
            column=str(col),
            dtype=str(series.dtype),
            missing=int(series.isna().sum()),
            unique=int(series.nunique()),
        )
        if pd.api.types.is_numeric_dtype(series) and series.notna().any():
            summary.mean = float(series.mean())
            summary.std = float(series.std()) if len(series) > 1 else 0.0
            summary.min = float(series.min())
            summary.max = float(series.max())
        columns.append(summary)

    return DatasetSummary(dataset=name, rows=len(frame), columns=columns)


@router.get("/{name}/export.csv")
def export_csv(name: str, frame: pd.DataFrame = Depends(get_dataset)):
    """Stream the whole dataset back as a CSV download.

    Generated row by row, so memory use does not grow with the dataset.
    """

    def rows():
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        writer.writerow(frame.columns)
        yield buffer.getvalue()

        for record in frame.itertuples(index=False):
            buffer.seek(0), buffer.truncate(0)
            writer.writerow(record)
            yield buffer.getvalue()

    return StreamingResponse(
        rows(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{name}.csv"'},
    )
