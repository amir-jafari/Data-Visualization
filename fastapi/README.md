# ⚡ Learn FastAPI

The other half of the course. [`streamlit/`](../streamlit/) builds the page a
person looks at; this builds the service behind it — the thing that holds the
data, runs the model, and answers over HTTP.

Same shape as the Streamlit course: small runnable files, one idea each,
building to a real project.

---

## Start here

```bash
pip install -r fastapi/requirements.txt

python fastapi/run.py                     # what is available, in reading order
python fastapi/run.py endpoints/hello     # run the first lesson
```

Open <http://127.0.0.1:8000/docs>. That interactive page is generated from your
code, and it is where you should try every endpoint in this course.

> **FastAPI is not installed on the course server yet** — everything it depends
> on already is. `pip install fastapi` is the only new package you need.

---

## What's in here

| | |
| --- | --- |
| **`run.py`** | Lists the lessons and runs one with auto-reload. |
| **`basics/`** | 25 one-idea-per-file lessons. [Details →](basics/README.md) |
| **`project/`** | The Data API: all of it, assembled, plus a Streamlit client. [Details →](project/README.md) |

---

## The path through it

**1. Work through `basics/` in order.** Eight chapters, each assuming the last:
routes → models → errors → structure → async → security → files → testing.
Every file runs on its own and serves its own `/docs`.

**2. Then read `project/`.** The same ideas, in the arrangement a real project
uses: a package with routers, dependencies, settings and tests. Its README maps
each file back to the lesson it came from.

**3. Then run both halves together.**

```bash
python fastapi/project/serve.py                # the API,     port 8000
streamlit run fastapi/project/client.py        # the client,  port 8501
```

That pair is the thing worth understanding. The API knows about data and
models and nothing about screens. The client knows about screens and nothing
about data. Either can be replaced without touching the other, and that is
what makes an API worth writing.

---

## How this connects to the Streamlit course

A Streamlit app is one process doing everything: loading data, running the
model, drawing the page. That is perfect for a demo and awkward for anything
shared — every user runs their own copy of the model.

Splitting it means the model loads once, in one place, and everyone talks to
it. The same ideas turn up on both sides under different names:

| Streamlit | FastAPI |
| --- | --- |
| `@st.cache_resource` — load the model once | a `lifespan` handler — train it at startup |
| `@st.cache_data` — don't redo slow work | `@lru_cache` in `store.py` |
| `st.session_state` | nothing — HTTP is stateless, which is why tokens exist |
| the script re-runs top to bottom | one function per route, run on demand |

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'fastapi'`** — `pip install -r
fastapi/requirements.txt`.

**`Address already in use`** — a previous lesson is still running. Stop it with
Ctrl-C, or use another port: `--port 8001`.

**`attempted relative import with no known parent package`** — you ran
`python fastapi/project/data_api/main.py`. Use `python fastapi/project/serve.py`;
`project/README.md` explains why.

**The client says the API is not running** — it is not. Start
`python fastapi/project/serve.py` in another terminal.

**A browser call fails but curl works** — CORS. See
`basics/files/static_and_cors.py`.
