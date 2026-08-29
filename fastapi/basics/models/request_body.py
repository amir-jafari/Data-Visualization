"""
Request bodies -- accepting data instead of just returning it.

What it shows:
    * a Pydantic model as a parameter means "read this from the JSON body"
    * the model validates the incoming data before your function ever runs
    * POST/PUT/DELETE are declared exactly like GET
    * body, path and query parameters can be mixed in one function

This is the moment FastAPI starts earning its keep. You describe the shape of
the data once, as a class, and get parsing, validation, error messages and
documentation from that single description.

Run it:
    python fastapi/basics/models/request_body.py

Try it from /docs -- click POST /items, "Try it out", and edit the JSON.
Or:
    curl -X POST http://127.0.0.1:8000/items \
         -H "Content-Type: application/json" \
         -d '{"name": "Laptop", "price": 999.99}'
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Request bodies")


class Item(BaseModel):
    """The shape of an item, described once and reused everywhere.

    `name` and `price` are required. `description` and `tax` are optional,
    because they have defaults.
    """
    name: str
    price: float
    description: str | None = None
    tax: float | None = None


@app.post("/items")
def create_item(item: Item):
    """`item: Item` means "parse the request body into this class".

    By the time this line runs, the data is valid. There is no `if not name:`
    check to write -- a bad request never reaches the function.
    """
    total = item.price + (item.tax or 0)
    return {"item": item, "total_with_tax": round(total, 2)}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, notify: bool = False):
    """Three kinds of input in one signature, and FastAPI sorts them out.

    `item_id` is in the path, so it is a path parameter.
    `item` is a Pydantic model, so it is the body.
    `notify` is a simple type that is not in the path, so it is a query param.
    """
    return {"item_id": item_id, "updated": item, "notified": notify}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"deleted": item_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
