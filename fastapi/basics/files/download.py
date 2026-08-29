"""
Downloads -- sending a file back, and building one on the fly.

What it shows:
    * FileResponse for a file that exists on disk
    * StreamingResponse for data you generate as you go
    * the Content-Disposition header, which is what makes a browser save
      the file instead of displaying it
    * returning a CSV or JSON export of a query -- the common data-app need

Run it:
    python fastapi/basics/files/download.py

Try:
    http://127.0.0.1:8000/export.csv
    http://127.0.0.1:8000/export.csv?rows=100000     (streamed, not buffered)
"""

import csv
import io
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

app = FastAPI(title="Downloads")

HERE = Path(__file__).resolve().parent
ROWS = [{"id": i, "name": f"item-{i}", "price": round(i * 1.5, 2)} for i in range(1, 21)]


@app.get("/export.csv")
def export_csv(rows: int = 20):
    """Generated in memory, then sent as a download.

    `media_type` tells the client what it is; the Content-Disposition header
    tells the browser to save it under that filename.
    """
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["id", "name", "price"])
    writer.writeheader()
    for i in range(1, rows + 1):
        writer.writerow({"id": i, "name": f"item-{i}", "price": round(i * 1.5, 2)})

    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="export.csv"'},
    )


@app.get("/stream.csv")
def stream_csv(rows: int = 100_000):
    """The version that scales: rows are produced one at a time.

    Nothing large is ever held in memory, and the client starts receiving data
    immediately instead of waiting for the whole file to be built.
    """

    def generate():
        yield "id,name,price\n"
        for i in range(1, rows + 1):
            yield f"{i},item-{i},{round(i * 1.5, 2)}\n"

    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="stream.csv"'},
    )


@app.get("/export.json")
def export_json():
    """JSONResponse when you want to set headers on an otherwise normal reply."""
    return JSONResponse(
        content=ROWS,
        headers={"Content-Disposition": 'attachment; filename="export.json"'},
    )


@app.get("/logo")
def logo():
    """FileResponse for something already on disk.

    It handles the content type, the length, and range requests for you.
    """
    path = HERE / "static" / "index.html"
    return FileResponse(path, media_type="text/html", filename="index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
