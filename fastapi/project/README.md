# project — the Data API

Everything from `basics/`, assembled into one service that does real work:
it serves the course datasets, and it serves predictions from a trained model.

```bash
# terminal 1 — the API
python fastapi/project/serve.py

# terminal 2 — a front end for it
streamlit run fastapi/project/client.py
```

Then open <http://127.0.0.1:8000/docs> and <http://localhost:8501>.

## What is where

| File | What it is | Lesson it came from |
| --- | --- | --- |
| `data_api/main.py` | Assembles the app: routers, CORS, lifespan, error handler | `structure/routers` |
| `data_api/config.py` | Settings from the environment | `structure/settings` |
| `data_api/schemas.py` | Every shape the API accepts or returns | `models/*` |
| `data_api/deps.py` | API key, pagination, dataset lookup | `structure/dependencies` |
| `data_api/store.py` | Where data comes from: S3, else built-in | — |
| `data_api/model.py` | The model, trained once at startup | `async_work` (lifespan) |
| `data_api/routers/` | One file per resource | `structure/routers` |
| `data_api/tests/` | 12 tests, no server and no S3 needed | `testing/*` |
| `client.py` | Streamlit front end that calls the API | — |
| `serve.py` | Starts the API | — |

## The endpoints

| Route | Does | Key? |
| --- | --- | --- |
| `GET /health` | Is it up, is the model loaded, is S3 reachable | no |
| `GET /datasets` | The catalogue | no |
| `GET /datasets/{name}` | A page of rows, filtered and sorted | no |
| `GET /datasets/{name}/summary` | Per-column statistics | no |
| `GET /datasets/{name}/export.csv` | The whole thing, streamed | no |
| `GET /model/info` | What the model expects | no |
| `POST /model/predict` | Predictions for a batch of rows | **yes** |

The key defaults to `student-key`. Change it with `API_API_KEY=...`.

## It works with no setup

`store.py` prefers the course S3 bucket and falls back to datasets that ship
with scikit-learn. No AWS keys, no network, still a working API — `/health`
tells you which source you got.

## The point of the client

Open `client.py` and notice what is *not* in it: no pandas loading, no S3, no
model. It asks the API over HTTP and draws the answer. That split is why the
same API can serve this page, a notebook, or somebody else's script — and why
you can rewrite either side without touching the other.

## Running the tests

```bash
pytest fastapi/project/data_api/tests/test_api.py
python fastapi/project/data_api/tests/test_api.py   # if you have no pytest
```

They never touch S3 and never train the model — the store and the model are
swapped for fakes, which is what `testing/overriding_dependencies.py` teaches.
