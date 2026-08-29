"""
Overriding dependencies -- testing without the real database or API key.

What it shows:
    * app.dependency_overrides swaps a dependency for a fake, in tests only
    * how that lets you test protected routes without real credentials
    * replacing a data source with fixed data, so tests are deterministic
    * cleaning up the override afterwards, so tests do not leak into each other

This is the practical pay-off of the dependencies lesson. Because your
endpoints ask for what they need rather than building it themselves, a test
can hand them something else.

Run it:
    python fastapi/basics/testing/overriding_dependencies.py
    pytest fastapi/basics/testing/overriding_dependencies.py
"""

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.testclient import TestClient

# --- the app ---------------------------------------------------------------
app = FastAPI(title="Dependency overrides")


def get_database():
    """In real life this opens a connection. In a test we never want it to."""
    raise RuntimeError("the real database is not available here")


def get_current_user(x_api_key: str = Header(default="")):
    """In real life this checks a key against a store."""
    if x_api_key != "the-real-production-key":
        raise HTTPException(401, "Invalid API key")
    return {"username": "real-user", "is_admin": False}


@app.get("/rows")
def read_rows(db=Depends(get_database)):
    return {"rows": db["rows"]}


@app.get("/me")
def read_me(user: dict = Depends(get_current_user)):
    return user


@app.delete("/rows")
def delete_rows(user: dict = Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(403, "Admins only")
    return {"deleted": True}


# --- the fakes -------------------------------------------------------------
def fake_database():
    return {"rows": [{"id": 1}, {"id": 2}, {"id": 3}]}


def fake_user():
    return {"username": "test-user", "is_admin": False}


def fake_admin():
    return {"username": "test-admin", "is_admin": True}


client = TestClient(app)


def test_without_override_the_real_dependency_runs():
    """Proof that the override is doing something: unpatched, this fails."""
    quiet = TestClient(app, raise_server_exceptions=False)
    assert quiet.get("/rows").status_code == 500


def test_fake_database():
    app.dependency_overrides[get_database] = fake_database
    try:
        response = client.get("/rows")
        assert response.status_code == 200
        assert len(response.json()["rows"]) == 3
    finally:
        # Always undo it. An override left behind will quietly change the
        # result of every test that runs after this one.
        app.dependency_overrides.clear()


def test_protected_route_without_a_real_key():
    app.dependency_overrides[get_current_user] = fake_user
    try:
        assert client.get("/me").json()["username"] == "test-user"
        assert client.delete("/rows").status_code == 403      # not an admin
    finally:
        app.dependency_overrides.clear()


def test_admin_route():
    """Same endpoint, different fake -- that is the whole trick."""
    app.dependency_overrides[get_current_user] = fake_admin
    try:
        assert client.delete("/rows").json() == {"deleted": True}
    finally:
        app.dependency_overrides.clear()


def test_real_dependency_is_back():
    """After cleanup, the real one is in force again."""
    assert client.get("/me").status_code == 401


if __name__ == "__main__":
    order = ["test_without_override_the_real_dependency_runs", "test_fake_database",
             "test_protected_route_without_a_real_key", "test_admin_route",
             "test_real_dependency_is_back"]
    for name in order:
        globals()[name]()
        print(f"  PASS  {name}")
    print(f"\n{len(order)} checks passed.")
