"""
Tests for the Data API.

Run them:
    pytest fastapi/project/data_api/tests/test_api.py
    python fastapi/project/data_api/tests/test_api.py     # no pytest needed

What is worth copying from this file:

  * every test uses a fake dataset store, so the suite never touches S3 and
    gives the same answer on a plane as it does on the server
  * the API key comes from settings, and settings are a dependency, so a test
    can set its own key instead of knowing the real one
  * the failure paths (404, 401, 422) are tested as carefully as the happy path
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi.testclient import TestClient          # noqa: E402

from data_api import model as model_module         # noqa: E402
from data_api import store                         # noqa: E402
from data_api.config import Settings, get_settings  # noqa: E402
from data_api.main import app                      # noqa: E402

# --- fixtures, hand-rolled so this runs with or without pytest -------------
FAKE = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "colour": ["red", "blue", "red", "green"],
    "score": [10.0, 20.0, 30.0, None],
})

TEST_KEY = "key-used-only-in-tests"


def fake_settings():
    return Settings(api_key=TEST_KEY, page_size=2, max_page_size=3)


def use_fake_store(monkey: dict):
    """Point the store at FAKE instead of S3, and remember what to undo."""
    monkey["names"] = store.names
    monkey["load"] = store.load
    monkey["source_of"] = store.source_of
    store.names = lambda: ["fake"]
    store.load = lambda name: FAKE.copy() if name == "fake" else None
    store.source_of = lambda name: "built-in"


def restore_store(monkey: dict):
    store.names, store.load, store.source_of = monkey["names"], monkey["load"], monkey["source_of"]


def make_client() -> TestClient:
    app.dependency_overrides[get_settings] = fake_settings
    return TestClient(app)


# --- tests -----------------------------------------------------------------
def test_root_and_health():
    client = make_client()
    assert client.get("/").status_code == 200
    body = client.get("/health").json()
    assert body["status"] == "ok"
    app.dependency_overrides.clear()


def test_dataset_listing_uses_the_store():
    monkey = {}
    use_fake_store(monkey)
    client = make_client()
    try:
        body = client.get("/datasets").json()
        assert [d["name"] for d in body] == ["fake"]
        assert body[0]["rows"] == 4
    finally:
        restore_store(monkey)
        app.dependency_overrides.clear()


def test_paging_respects_settings():
    """page_size is 2 in fake_settings, so an unasked-for page has 2 rows."""
    monkey = {}
    use_fake_store(monkey)
    client = make_client()
    try:
        body = client.get("/datasets/fake").json()
        assert body["total"] == 4
        assert body["returned"] == 2

        # and max_page_size (3) caps a greedy request
        assert client.get("/datasets/fake?limit=100").json()["returned"] == 3

        second = client.get("/datasets/fake?limit=2&offset=2").json()
        assert second["rows"][0]["id"] == 3
    finally:
        restore_store(monkey)
        app.dependency_overrides.clear()


def test_filtering_and_sorting():
    monkey = {}
    use_fake_store(monkey)
    client = make_client()
    try:
        body = client.get("/datasets/fake?column=colour&equals=red").json()
        assert body["total"] == 2

        body = client.get("/datasets/fake?sort_by=score&descending=true").json()
        assert body["rows"][0]["score"] == 30.0

        assert client.get("/datasets/fake?column=nope&equals=x").status_code == 422
    finally:
        restore_store(monkey)
        app.dependency_overrides.clear()


def test_missing_values_become_null_not_nan():
    """NaN is not valid JSON. If this regresses, clients break on parse."""
    monkey = {}
    use_fake_store(monkey)
    client = make_client()
    try:
        response = client.get("/datasets/fake?limit=3&offset=3")
        assert response.status_code == 200
        assert response.json()["rows"][0]["score"] is None
    finally:
        restore_store(monkey)
        app.dependency_overrides.clear()


def test_unknown_dataset_is_404():
    monkey = {}
    use_fake_store(monkey)
    client = make_client()
    try:
        response = client.get("/datasets/does-not-exist")
        assert response.status_code == 404
        assert "does-not-exist" in response.json()["detail"]
    finally:
        restore_store(monkey)
        app.dependency_overrides.clear()


def test_summary():
    monkey = {}
    use_fake_store(monkey)
    client = make_client()
    try:
        body = client.get("/datasets/fake/summary").json()
        score = next(c for c in body["columns"] if c["column"] == "score")
        assert score["missing"] == 1
        assert score["max"] == 30.0
        colour = next(c for c in body["columns"] if c["column"] == "colour")
        assert colour["unique"] == 3 and colour["mean"] is None
    finally:
        restore_store(monkey)
        app.dependency_overrides.clear()


def test_csv_export():
    monkey = {}
    use_fake_store(monkey)
    client = make_client()
    try:
        response = client.get("/datasets/fake/export.csv")
        assert response.status_code == 200
        assert "attachment" in response.headers["content-disposition"]
        lines = response.text.strip().splitlines()
        assert lines[0].startswith("id,colour,score")
        assert len(lines) == 5                       # header + 4 rows
    finally:
        restore_store(monkey)
        app.dependency_overrides.clear()


def test_predict_requires_a_key():
    client = make_client()
    try:
        payload = {"rows": [{"mean radius": 14.0}]}
        assert client.post("/model/predict", json=payload).status_code == 401
        assert client.post("/model/predict", json=payload,
                           headers={"X-API-Key": "wrong"}).status_code == 401
    finally:
        app.dependency_overrides.clear()


class _StubModel:
    """Stands in for the trained model, so no test ever fits one.

    TestClient does not run the lifespan handler unless you use it as a
    context manager, so the real model is never trained here -- which is
    exactly what keeps this suite fast and offline.
    """
    estimator = type("Stub", (), {})()
    features = ["a", "b"]
    target_names = ["benign", "malignant"]
    accuracy = 0.99
    trained_on = "stub"

    def predict(self, rows):
        return [("benign", 0.87) for _ in rows]


def test_predict_with_a_fake_model():
    original = model_module.get_model()
    model_module.set_model(_StubModel())
    client = make_client()
    try:
        response = client.post(
            "/model/predict",
            json={"rows": [{"a": 1.0, "b": 2.0}, {"a": 3.0, "b": 4.0}]},
            headers={"X-API-Key": TEST_KEY},
        )
        assert response.status_code == 200
        body = response.json()
        assert len(body["predictions"]) == 2
        assert body["predictions"][0]["prediction"] == "benign"

        assert client.get("/model/info").json()["n_features"] == 2
    finally:
        model_module.set_model(original)
        app.dependency_overrides.clear()


def test_predict_rejects_an_empty_batch():
    """422 for a bad body -- but only once a model exists.

    Worth understanding: dependencies are resolved before the body is
    validated, so with no model loaded this route answers 503 and the 422
    never happens. A test that forgot the stub would "pass" for the wrong
    reason, or fail confusingly. Install the stub, then assert.
    """
    original = model_module.get_model()
    model_module.set_model(_StubModel())
    client = make_client()
    try:
        response = client.post("/model/predict", json={"rows": []},
                               headers={"X-API-Key": TEST_KEY})
        assert response.status_code == 422, response.status_code
    finally:
        model_module.set_model(original)
        app.dependency_overrides.clear()


def test_missing_model_is_503():
    original = model_module.get_model()
    model_module.set_model(None)
    client = make_client()
    try:
        assert client.get("/model/info").status_code == 503
    finally:
        model_module.set_model(original)
        app.dependency_overrides.clear()


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
        print(f"  PASS  {test.__name__}")
    print(f"\n{len(tests)} tests passed.")
