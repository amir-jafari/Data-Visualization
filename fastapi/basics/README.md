# basics — one idea per file

Every file here is a complete, runnable API. Read it, run it, poke it in
`/docs`, then change something and watch what happens.

```bash
python fastapi/run.py                    # the list, in reading order
python fastapi/run.py endpoints/hello    # run one, with auto-reload
python fastapi/basics/endpoints/hello.py # or just run the file
```

Every lesson serves its own docs at <http://127.0.0.1:8000/docs>. That page is
the fastest way to try an endpoint — no curl, no Postman.

| Chapter | You learn |
| --- | --- |
| `endpoints` | Routes, and the three places their values come from: path, query, headers |
| `models` | Describing data once with Pydantic, and getting validation + docs from it |
| `errors` | Status codes, `HTTPException`, and one consistent error shape |
| `structure` | Routers, dependencies and settings — how a real project is laid out |
| `async_work` | `def` vs `async def`, background tasks, doing several things at once |
| `security` | API keys, and an OAuth2 password login with tokens and scopes |
| `files` | Uploads, downloads, static files, and why CORS bites you |
| `testing` | Testing an API in-process, and faking its dependencies |

Read them in that order — each chapter assumes the one before it.

For the ideas behind these files — analogies, demos and the mistakes students
make — see [`../CONCEPTS.md`](../CONCEPTS.md).

## Three things worth knowing early

**The type hints are not decoration.** `item_id: int` converts the value,
rejects bad input with a 422, and documents the endpoint. Almost every feature
in this course is FastAPI reading your function signature and acting on it.

**`/docs` is generated, not written.** If an endpoint looks wrong there, the
signature is wrong. It is a debugging tool as much as documentation.

**`def` unless you `await`.** A plain `def` endpoint runs in a thread pool and
may block safely. An `async def` that blocks freezes the server for everyone.
`async_work/sync_vs_async.py` shows the difference with a stopwatch.

## Naming a new lesson

Don't name a lesson file after a package you can import. A lesson called
`json.py` or `requests.py` sits in a folder that ends up on Python's import
path, so `import json` finds your lesson instead of the library and everything
breaks in a confusing way. (The Streamlit half of this repo learned that the
hard way — see `streamlit/basics/README.md`.)
