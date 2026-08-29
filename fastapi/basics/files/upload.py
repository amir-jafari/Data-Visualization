"""
File uploads -- receiving a file instead of JSON.

What it shows:
    * UploadFile for the file itself, Form() for fields sent alongside it
    * why UploadFile beats `bytes` for anything that might be large
    * checking the type and size *before* trusting the contents
    * reading an uploaded CSV straight into pandas

Uploads arrive as multipart/form-data, not JSON, which is why this needs the
`python-multipart` package.

Run it:
    python fastapi/basics/files/upload.py

Easiest from /docs -- POST /upload has a file picker. Or:
    curl -F "file=@yourfile.csv" http://127.0.0.1:8000/upload/csv
"""

import io

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

app = FastAPI(title="File uploads")

MAX_BYTES = 5 * 1024 * 1024        # 5 MB


@app.post("/upload")
async def upload(file: UploadFile):
    """UploadFile is streamed to a temporary file, not held in memory.

    Declaring `file: bytes` instead would read the whole thing into RAM --
    fine for a small image, fatal for a 2 GB upload.
    """
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
    }


@app.post("/upload/with-fields")
async def upload_with_fields(
    file: UploadFile = File(description="The file to attach"),
    description: str = Form(),
    tags: str = Form(default=""),
):
    """Files and normal fields together.

    Note `Form()`, not the usual body model: once a request is multipart, the
    other fields come from the form too, not from JSON.
    """
    contents = await file.read()
    return {
        "filename": file.filename,
        "description": description,
        "tags": [t for t in tags.split(",") if t],
        "size_bytes": len(contents),
    }


@app.post("/upload/many")
async def upload_many(files: list[UploadFile]):
    """A list of UploadFile accepts several files under the same field name."""
    return [{"filename": f.filename, "size_bytes": len(await f.read())} for f in files]


@app.post("/upload/csv")
async def upload_csv(file: UploadFile):
    """Validate before you parse -- never trust an upload.

    Two checks, in this order: the name looks right, and the size is sane.
    Only then hand the bytes to a parser.
    """
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Only .csv files are accepted")

    contents = await file.read()
    if len(contents) > MAX_BYTES:
        raise HTTPException(413, f"File is larger than {MAX_BYTES // 1024 // 1024} MB")

    import pandas as pd

    try:
        frame = pd.read_csv(io.BytesIO(contents))
    except Exception as exc:
        raise HTTPException(400, f"Could not parse that as CSV: {exc}")

    # pandas is lenient -- it will happily read binary junk as a one-column
    # table rather than raising. So the try/except above is not the real
    # defence; checking that the result makes sense is.
    if frame.empty or len(frame.columns) == 0:
        raise HTTPException(400, "That file parsed, but contains no usable rows")

    return {
        "filename": file.filename,
        "rows": len(frame),
        "columns": list(frame.columns),
        "preview": frame.head(3).to_dict(orient="records"),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
