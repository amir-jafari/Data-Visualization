"""
Status codes -- the number that tells the client what happened.

What it shows:
    * status_code= on the decorator sets the default for a route
    * 201 for "created", 204 for "nothing to return", 200 for everything else
    * changing the code for one particular response
    * why you should use `status.HTTP_201_CREATED` instead of `201`

A client reads the status code before it reads the body. Getting it right is
what makes an API usable by something other than a human.

Run it:
    python fastapi/basics/errors/status_codes.py
    curl -i -X POST http://127.0.0.1:8000/items -H "Content-Type: application/json" -d '{"name":"x"}'
"""

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI(title="Status codes")

ITEMS: dict[int, str] = {1: "already here"}


class Item(BaseModel):
    name: str


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    """201 Created, not 200 OK -- something new now exists.

    `status.HTTP_201_CREATED` is just the number 201, but it says what it
    means, and your editor can autocomplete it.
    """
    new_id = max(ITEMS) + 1 if ITEMS else 1
    ITEMS[new_id] = item.name
    return {"id": new_id, "name": item.name}


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """204 means "done, and there is deliberately no body". So return nothing."""
    ITEMS.pop(item_id, None)
    return None


@app.put("/items/{item_id}")
def upsert_item(item_id: int, item: Item, response: Response):
    """One route, two possible codes -- decided at runtime.

    Created something new? 201. Updated something that existed? 200.
    """
    existed = item_id in ITEMS
    ITEMS[item_id] = item.name
    response.status_code = status.HTTP_200_OK if existed else status.HTTP_201_CREATED
    return {"id": item_id, "updated": existed}


@app.get("/items")
def list_items():
    """The default. You only declare a status code when it is not 200."""
    return ITEMS


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
