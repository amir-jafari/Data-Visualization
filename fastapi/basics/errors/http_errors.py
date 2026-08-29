"""
HTTPException -- failing on purpose, clearly.

What it shows:
    * raise HTTPException(...) to stop and return an error
    * choosing the right code: 404 missing, 400 bad request, 403 not allowed,
      409 conflict
    * adding headers to an error response
    * why raising beats returning an error dict

Returning `{"error": "not found"}` with a 200 is the most common beginner
mistake in web APIs: the client's `if response.ok` check passes, and the bug
surfaces somewhere far away. Raise instead.

Run it:
    python fastapi/basics/errors/http_errors.py
    curl -i http://127.0.0.1:8000/items/999
"""

from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="HTTP errors")

ITEMS = {1: {"name": "Notebook", "owner": "ada"}, 2: {"name": "Pen", "owner": "bob"}}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    """404 when the thing simply is not there."""
    if item_id not in ITEMS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} does not exist",
        )
    return ITEMS[item_id]


@app.delete("/items/{item_id}")
def delete_item(item_id: int, user: str = "guest"):
    """403 when it exists, but this caller may not touch it.

    404 and 403 answer different questions: "is it there?" and "are you
    allowed?". Sending the wrong one either leaks information or confuses.
    """
    item = ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Item {item_id} does not exist")
    if item["owner"] != user:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Item {item_id} belongs to {item['owner']}, not {user}",
        )
    del ITEMS[item_id]
    return {"deleted": item_id}


@app.post("/items/{item_id}")
def create_item(item_id: int, name: str):
    """409 Conflict -- the request was fine, but it clashes with reality."""
    if item_id in ITEMS:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Item {item_id} already exists")
    ITEMS[item_id] = {"name": name, "owner": "guest"}
    return ITEMS[item_id]


@app.get("/protected")
def protected(token: str | None = None):
    """401 with a WWW-Authenticate header -- the polite way to demand a login."""
    if token != "letmein":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"secret": "the cake is a lie"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
