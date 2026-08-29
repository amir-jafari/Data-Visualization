"""
Testing -- calling your API in-process, with no server running.

What it shows:
    * TestClient sends real requests through your app, without a network
    * asserting on the status code AND the body, not just "it didn't crash"
    * testing the failure paths, which is where bugs actually live
    * two gotchas that surprise everyone the first time

This file is both a lesson and a real test suite. Run it either way:

    python fastapi/basics/testing/test_client.py     # runs the checks, prints
    pytest fastapi/basics/testing/test_client.py     # if you have pytest

Gotcha 1: TestClient runs background tasks *before* returning, so a background
task looks slow in a test and instant in production.

Gotcha 2: by default TestClient re-raises exceptions from your app instead of
returning the 500 your users would see. Pass raise_server_exceptions=False
when you are specifically testing an error handler.
"""

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

# --- the app under test ----------------------------------------------------
app = FastAPI(title="Testing")

ITEMS: dict[int, str] = {1: "notebook"}


class Item(BaseModel):
    name: str


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in ITEMS:
        raise HTTPException(404, f"No item {item_id}")
    return {"id": item_id, "name": ITEMS[item_id]}


@app.post("/items", status_code=201)
def create_item(item: Item):
    new_id = max(ITEMS) + 1 if ITEMS else 1
    ITEMS[new_id] = item.name
    return {"id": new_id, "name": item.name}


@app.get("/boom")
def boom():
    raise RuntimeError("deliberate bug")


# --- the tests -------------------------------------------------------------
client = TestClient(app)


def test_read_existing_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "notebook"}


def test_missing_item_is_404():
    """The failure path matters as much as the happy one."""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "No item 999" in response.json()["detail"]


def test_bad_type_is_422():
    """You did not write this validation, but you should still test it --
    it is part of your API's contract with its callers."""
    response = client.get("/items/not-a-number")
    assert response.status_code == 422


def test_create_item():
    response = client.post("/items", json={"name": "pencil"})
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "pencil"

    # and it is really there afterwards
    assert client.get(f"/items/{created['id']}").status_code == 200


def test_missing_body_field_is_422():
    assert client.post("/items", json={}).status_code == 422


def test_unhandled_error_becomes_500():
    """Gotcha 2 in action: without this flag, the RuntimeError would escape
    the client and fail the test instead of becoming a response."""
    quiet = TestClient(app, raise_server_exceptions=False)
    assert quiet.get("/boom").status_code == 500


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print(f"  PASS  {test.__name__}")
    print(f"\n{len(tests)} checks passed.")
