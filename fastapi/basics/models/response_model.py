"""
Response models -- controlling what goes back out.

What it shows:
    * `response_model=` declares the shape of the reply
    * fields not in the response model are dropped -- this is how you avoid
      leaking a password hash by accident
    * the reply is documented in /docs, so callers know what to expect
    * response_model_exclude_none tidies away empty fields

The important idea: input and output are *different shapes*, and saying so
explicitly is what keeps private fields private.

Run it:
    python fastapi/basics/models/response_model.py

Try POST /users -- you send a password, and the reply does not contain one.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Response models")


class UserIn(BaseModel):
    """What the client sends -- including a password."""
    username: str
    password: str
    email: str
    full_name: str | None = None


class UserOut(BaseModel):
    """What we send back -- deliberately no password field."""
    username: str
    email: str
    full_name: str | None = None


FAKE_DB: dict[str, UserIn] = {}


@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    """Note what is returned: the whole `user`, password and all.

    FastAPI filters it through UserOut on the way out, so the password never
    reaches the client. The safety comes from the declaration, not from
    remembering to strip the field by hand.
    """
    FAKE_DB[user.username] = user
    return user


@app.get("/users/{username}", response_model=UserOut)
def read_user(username: str):
    return FAKE_DB.get(username, UserIn(username=username, password="", email="unknown"))


class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    tags: list[str] = []


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_none=True)
def read_item(item_id: int):
    """exclude_none drops keys whose value is None, instead of sending nulls."""
    return Item(name=f"item-{item_id}", price=9.99)


@app.get("/items", response_model=list[Item])
def list_items():
    """A response model can be a list, and /docs will say so."""
    return [Item(name="one", price=1.0), Item(name="two", price=2.0, tags=["sale"])]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
