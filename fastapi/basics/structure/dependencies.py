"""
Dependencies -- shared setup, declared instead of repeated.

What it shows:
    * Depends(f) means "call f first, and pass me the result"
    * a dependency can take parameters -- they appear in /docs too
    * dependencies can depend on other dependencies
    * `yield` for setup/teardown, which is how database sessions work
    * a class as a dependency, when it needs configuration

This is FastAPI's central idea and the one worth spending time on. Anything
several endpoints need -- pagination arguments, the current user, a database
connection -- becomes a small function they all declare.

Run it:
    python fastapi/basics/structure/dependencies.py
"""

from fastapi import Depends, FastAPI, Header, HTTPException, Query

app = FastAPI(title="Dependencies")

ITEMS = [{"id": i, "name": f"item-{i}"} for i in range(1, 101)]


# --- 1. a plain function of shared parameters ------------------------------
def pagination(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Three endpoints want paging. Describe it once, here."""
    return {"limit": limit, "offset": offset}


@app.get("/items")
def list_items(page: dict = Depends(pagination)):
    """`page` is whatever pagination() returned.

    The limit/offset query parameters still show up in /docs -- FastAPI reads
    the dependency's signature as well as the endpoint's.
    """
    return ITEMS[page["offset"]:page["offset"] + page["limit"]]


@app.get("/users")
def list_users(page: dict = Depends(pagination)):
    """The same three lines of paging logic, not written a second time."""
    return {"page": page, "users": []}


# --- 2. dependencies that depend on dependencies ---------------------------
def get_token(x_token: str = Header(default="")):
    if not x_token:
        raise HTTPException(401, "Missing X-Token header")
    return x_token


def get_current_user(token: str = Depends(get_token)):
    """Depends on get_token, which FastAPI resolves first.

    You get a chain: header -> token -> user. Each link is separately testable.
    """
    users = {"secret": "ada", "guest-token": "guest"}
    if token not in users:
        raise HTTPException(401, "Unknown token")
    return {"username": users[token], "is_admin": token == "secret"}


@app.get("/me")
def read_me(user: dict = Depends(get_current_user)):
    return user


@app.get("/admin")
def admin_only(user: dict = Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(403, "Admins only")
    return {"message": f"Welcome, {user['username']}"}


# --- 3. yield: setup before, teardown after --------------------------------
OPEN_CONNECTIONS: list[str] = []


def get_connection():
    """Everything before `yield` runs on the way in; after, on the way out.

    This is the shape of a real database session: open it, hand it over, and
    close it afterwards -- even if the endpoint raised.
    """
    connection = f"connection-{len(OPEN_CONNECTIONS) + 1}"
    OPEN_CONNECTIONS.append(connection)
    try:
        yield connection
    finally:
        OPEN_CONNECTIONS.remove(connection)


@app.get("/query")
def run_query(connection: str = Depends(get_connection)):
    return {"used": connection, "open_during_request": len(OPEN_CONNECTIONS)}


@app.get("/connections")
def count_connections():
    """Always 0 -- every connection was closed when its request finished."""
    return {"still_open": len(OPEN_CONNECTIONS)}


# --- 4. a class as a dependency, when it needs configuring -----------------
class RateLimit:
    """Instances are callable, so an instance can be a dependency.

    Use this when the dependency itself needs settings -- here, how many calls
    are allowed.
    """

    def __init__(self, max_calls: int):
        self.max_calls = max_calls
        self.seen: dict[str, int] = {}

    def __call__(self, x_client: str = Header(default="anonymous")):
        self.seen[x_client] = self.seen.get(x_client, 0) + 1
        if self.seen[x_client] > self.max_calls:
            raise HTTPException(429, f"Limit of {self.max_calls} calls reached")
        return self.seen[x_client]


limit_3 = RateLimit(max_calls=3)


@app.get("/limited")
def limited(call_number: int = Depends(limit_3)):
    """Call this four times with the same X-Client header. The fourth is 429."""
    return {"call_number": call_number}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
