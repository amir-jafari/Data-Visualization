"""
Routers -- splitting a growing API into pieces.

What it shows:
    * APIRouter is "a FastAPI app you can include in another one"
    * prefix= and tags= applied once, to a whole group of routes
    * app.include_router() to wire them together
    * a dependency applied to an entire router at once

One file per resource is how every real FastAPI project is laid out. Both
routers live in this single file so you can see the whole picture at once --
`fastapi/project/data_api/` shows the same thing split across real files,
which is the version to copy.

Run it:
    python fastapi/basics/structure/routers.py

Look at /docs: the routes are grouped under "users" and "items" headings.
That grouping is what tags= bought you.
"""

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

# --- one router per resource ----------------------------------------------
users = APIRouter(prefix="/users", tags=["users"])


@users.get("")
def list_users():
    """The path is "" here, so the full path is just the prefix: /users"""
    return [{"id": 1, "name": "ada"}, {"id": 2, "name": "bob"}]


@users.get("/{user_id}")
def read_user(user_id: int):
    """Full path: /users/{user_id}. The prefix is added for you."""
    return {"id": user_id, "name": f"user-{user_id}"}


# --- a second resource -----------------------------------------------------
items = APIRouter(prefix="/items", tags=["items"])


@items.get("")
def list_items():
    return [{"id": 1, "name": "notebook"}]


@items.post("", status_code=201)
def create_item(name: str):
    return {"id": 99, "name": name}


# --- a rule that should cover every route in a router ----------------------
def require_token(x_token: str = Header(default="")):
    """A dependency. The next lesson covers these properly -- for now, read it
    as "run this before the endpoint, and fail the request if it raises"."""
    if x_token != "secret":
        raise HTTPException(401, "Set an X-Token header of 'secret'")


# --- assemble --------------------------------------------------------------
app = FastAPI(title="Routers")

app.include_router(users)

# Attaching the dependency here applies it to every route in `items`, instead
# of repeating it on each one.
app.include_router(items, dependencies=[Depends(require_token)])


@app.get("/", tags=["root"])
def root():
    return {"routers": ["users", "items"], "hint": "/items needs X-Token: secret"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
