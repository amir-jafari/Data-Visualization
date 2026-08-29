"""
Path parameters -- values taken from inside the URL itself.

What it shows:
    * `{name}` in the path becomes an argument to your function
    * the type hint is not decoration: FastAPI converts and validates with it
    * a bad value produces a clear 422 error that you did not have to write
    * order matters -- a fixed path must be declared before a matching pattern

Run it:
    python fastapi/basics/endpoints/path_params.py

Try:
    http://127.0.0.1:8000/items/7          -> works, and 7 is an int
    http://127.0.0.1:8000/items/banana     -> 422, with a readable explanation
    http://127.0.0.1:8000/users/me         -> the fixed route, not user "me"
"""

from fastapi import FastAPI, Path

app = FastAPI(title="Path parameters")


@app.get("/items/{item_id}")
def read_item(item_id: int):
    """`item_id: int` is doing three jobs at once.

    It converts "7" (URL text is always text) into the integer 7, rejects
    anything that is not a number with a 422, and tells /docs that this
    endpoint takes an integer.
    """
    return {"item_id": item_id, "type": type(item_id).__name__}


# Declared BEFORE /users/{user_id}. Routes are matched top to bottom, so if the
# pattern came first it would swallow "me" and try to parse it as a user id.
@app.get("/users/me")
def read_current_user():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/products/{product_id}")
def read_product(
    # Path() lets you attach rules and documentation to the parameter.
    product_id: int = Path(ge=1, le=1000, description="Between 1 and 1000"),
):
    """Constraints live next to the parameter, and appear in /docs.

    Try /products/0 -- the error says exactly which rule was broken.
    """
    return {"product_id": product_id}


@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    """`:path` is the exception -- it allows slashes, for a whole path.

    Try /files/data/2024/report.csv
    """
    return {"file_path": file_path}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
