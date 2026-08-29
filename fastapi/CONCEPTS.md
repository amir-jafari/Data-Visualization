# The ideas behind the code

A plain-words companion to `fastapi/`. Every idea here points at a file you can
open and run, so you can say the sentence, then show the thing.

**How to use it.** Each section has the same four parts:

- **The idea** — one sentence you can say out loud
- **A picture** — an analogy that makes it stick
- **In the code** — the real file, and the lines that matter
- **Watch them trip** — the mistake students actually make

---

## 0. What is an API, and why bother?

**The idea.** An API is a program that answers questions over the network
instead of drawing a screen.

**A picture.** A restaurant. The kitchen has the food and knows the recipes.
You never walk into the kitchen — you talk to a waiter, in a fixed language
("table for two", "the fish, no salt"). The waiter is the API. The kitchen can
be rebuilt, the chef replaced, the menu reprinted, and you still order the same
way.

**Why this course has both halves.** Students already know Streamlit, so start
from what they know:

| | Streamlit app | FastAPI service |
| --- | --- | --- |
| Who is it for? | a person, with eyes | another program |
| What does it return? | pixels | JSON |
| Where does the model live? | in every user's session | in one place, loaded once |
| Ten users? | ten copies of the model | one copy, ten callers |

Say this out loud: *"A Streamlit app is one person's laptop. An API is a
service the whole class can share."*

That is the entire motivation. Everything else is detail.

---

## 1. The one idea that explains most of FastAPI

If students remember nothing else, make it this:

> **Your function signature is the specification.**
> FastAPI reads the way you wrote the function and does the rest.

Open `basics/endpoints/path_params.py`:

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "type": type(item_id).__name__}
```

That one type hint, `: int`, does **three jobs at once**:

1. **Converts** — URLs are always text, so `"7"` becomes the integer `7`
2. **Validates** — `/items/banana` is rejected with a clear 422 error you did
   not write
3. **Documents** — `/docs` now says this endpoint takes an integer

Show it live. Visit `/items/7`, then `/items/banana`, then `/docs`. Three
browser tabs, one idea.

**Watch them trip.** Students think type hints are comments — decoration that
Python ignores. Here they are the program. Delete the `: int` in front of the
class and show `/items/banana` suddenly "working" and returning a string.

---

## 2. Where a value can come from

**The idea.** A request carries values in three different places, and FastAPI
works out which is which from where you put the parameter.

**A picture.** A parcel. The **address on the outside** is the path. The
**sticky notes on the box** are the query string. The **customs form in the
plastic sleeve** is the headers. The **thing inside** is the body.

**In the code.** `basics/endpoints/` — one file per place:

| Where | Looks like | File |
| --- | --- | --- |
| Path | `/items/7` | `path_params.py` |
| Query | `/search?q=python&limit=5` | `query_params.py` |
| Headers | `X-API-Key: abc123` | `headers.py` |
| Body | the JSON you POST | `models/request_body.py` |

The rule FastAPI uses, worth writing on the board:

- Is the name in the path string? → **path parameter**
- Is it a Pydantic model? → **body**
- Otherwise → **query parameter**

`basics/models/request_body.py` has all three in one function, which is the
best single slide in the chapter:

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, notify: bool = False):
```

`item_id` is in the path. `item` is a model, so it is the body. `notify` is
neither, so it is `?notify=true`.

**Watch them trip.** They try to send JSON to a `GET` endpoint. Ask: *"Which
of the four places would that go in?"* GET requests have no body — that is why
search terms live in the query string.

---

## 3. Describe the data once (Pydantic)

**The idea.** Write a class that says what your data looks like. Get parsing,
validation, error messages and documentation from that one description.

**A picture.** A passport control desk. You do not argue with each traveller
individually; you hold up the rules once, and anyone who does not match never
reaches the country.

**In the code.** `basics/models/response_model.py` has the sharpest example in
the whole course:

```python
class UserIn(BaseModel):      # what the client sends
    username: str
    password: str
    email: str

class UserOut(BaseModel):     # what we send back -- no password field
    username: str
    email: str

@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    FAKE_DB[user.username] = user
    return user               # returns EVERYTHING, password included
```

Now the moment. Ask the class: *"We return the whole user, password and all.
Does the password reach the client?"*

Let them vote. Then run it. **No** — `response_model=UserOut` filters it on the
way out.

Say this: *"The password is safe because of a declaration, not because someone
remembered to delete it. That is the difference between a rule and a habit."*

**Watch them trip.** They write validation by hand inside the endpoint —
`if not name: return {"error": ...}`. Show them `basics/models/validation.py`
and count the `if` statements they no longer need.

---

## 4. Failing properly

**The idea.** The status code is the first thing a machine reads. Getting it
right is what makes your API usable by something other than a human.

**A picture.** A traffic light. Nobody reads a paragraph explaining the
junction; they read the colour. `200` = go, `404` = nothing here, `401` = who
are you, `403` = I know who you are and no, `500` = we broke.

**In the code.** `basics/errors/http_errors.py`. The one line to emphasise:

```python
raise HTTPException(404, f"Item {item_id} does not exist")
```

**Raise**, do not return. Then explain why with the counter-example students
have all written:

```python
return {"error": "not found"}     # sends 200 OK -- the light is GREEN
```

The caller's `if response.ok:` passes. The bug surfaces three files away.

Teach the difference between 404 and 403 as a pair of questions:

- **404** — "Is it there?" → no
- **403** — "Are you allowed?" → no

`basics/errors/custom_errors.py` goes one step further and is worth showing to
stronger students: business logic raises a plain Python exception that knows
nothing about HTTP (`InsufficientFunds`), and a handler at the edge turns it
into a response. That keeps the logic testable without a web server.

---

## 5. Dependencies — the heart of FastAPI

**The idea.** Anything several endpoints need, write once as a small function
and let them ask for it.

**A picture.** A hospital. Every doctor needs the patient's chart, a
thermometer and a washed pair of hands. You do not teach each doctor to build
a thermometer — those things are *provided* on the way in.

**In the code.** `basics/structure/dependencies.py`:

```python
def pagination(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    return {"limit": limit, "offset": offset}

@app.get("/items")
def list_items(page: dict = Depends(pagination)):
    return ITEMS[page["offset"]:page["offset"] + page["limit"]]
```

Point out the bit that surprises people: `limit` and `offset` **still appear in
`/docs`**. FastAPI read the dependency's signature too. The documentation
follows the code down as many levels as you nest it.

### The `yield` version

This is the one worth slowing down on, because it is how every real database
connection works:

```python
def get_connection():
    connection = open_one()
    try:
        yield connection      # <- the endpoint runs HERE
    finally:
        close(connection)     # <- runs afterwards, even if it crashed
```

Run the demo: `/query` reports 1 connection open during the request, and
`/connections` reports 0 afterwards. Every time.

**Say this:** *"Everything above `yield` is setup, everything below is cleanup,
and the endpoint happens in the gap."*

**Why it matters later.** Because endpoints *ask* for what they need instead of
building it, a test can hand them something else. That is section 9, and it is
the pay-off — flag it now so it lands later.

---

## 6. `def` or `async def` — the one people get wrong

**The idea.**

```
def         -> FastAPI runs it in a worker thread. Blocking is fine.
async def   -> runs on the shared event loop. Blocking freezes the WHOLE
               server, for every user.
```

**A picture.** A restaurant with one waiter (the event loop). The waiter takes
orders from everyone and never stands still. `await` means "go check on another
table while this cooks". A blocking call inside `async def` is the waiter
sitting down at table 4 and waiting for the food — nobody else gets served.

**In the code.** `basics/async_work/sync_vs_async.py` has all three versions of
the same slow endpoint. Do this live, with two terminals:

```bash
curl http://127.0.0.1:8000/blocking-async   # start this first
curl http://127.0.0.1:8000/quick            # ...this WAITS. Server is frozen.
```

Then the same with `/blocking-sync` — `/quick` answers instantly.

**The rule to write on the board:**

> Use `async def` **only** if the body actually says `await`.
> Otherwise use plain `def` and let FastAPI handle the threading.

For a data course that means: pandas, scikit-learn, `requests`, a normal
database driver → plain `def`, always.

### Why bother with async at all?

`basics/async_work/concurrency.py` answers it with a stopwatch. Four calls that
take one second each:

| Endpoint | Time |
| --- | --- |
| `/sequential` — await them one at a time | **4.0 s** |
| `/concurrent` — `asyncio.gather` them | **1.0 s** |

Those are the real measured numbers from that file. One slow call gains
nothing from async. Four that can overlap gain everything.

### Background tasks

`basics/async_work/background_tasks.py`: answer the client now, do the slow
follow-up afterwards.

```python
@app.post("/signup")
def signup(user: User, background: BackgroundTasks):
    background.add_task(send_welcome_email, user.email)
    return {"created": user.username}      # client gets this immediately
```

Measured against a real server: the reply takes **0.005 seconds**, and the
email task finishes **2 seconds later**. Show `/log` before and after.

**Watch them trip.** In a *test*, this looks like it takes the full 2 seconds,
because `TestClient` runs background tasks before returning. It is noted in the
file. Good moment to say: *"the test is not always the same as the world."*

---

## 7. Security — two kinds of "who are you?"

**The idea.** An API key identifies a **program**. A login identifies a
**person**.

**A picture.** A key card gets a delivery robot into the building. A passport
identifies you specifically, expires, and says which countries you may enter.

**In the code.**

`basics/security/api_key.py` — the simple one. A header, checked against a list,
wrapped in a dependency so a route just says "I need a key". One detail worth a
sentence: it compares with `compare_digest`, not `==`, so an attacker cannot
guess the key one character at a time by measuring how long the answer takes.

`basics/security/oauth2.py` — the real one. Log in once, get a **token**, send
the token afterwards. Two points to draw out:

1. **Passwords are never stored.** Only a hash. Show `hash_password` and ask
   *"if someone steals this database, do they have the passwords?"*
2. **The token is signed.** Change one character of the payload and the server
   rejects it. This is demonstrated by a test in the course that forges a token
   with extra permissions and gets a 401.

**Scopes** are the last idea: not just *who you are* but *what you may do*.
`ada` has `["read", "write"]` and can POST. `bob` has `["read"]` and gets a 403
on the same endpoint with a perfectly valid token.

**Watch them trip.** They put the API key in the URL: `?api_key=secret`. Ask
where URLs get written down — browser history, server logs, the link they paste
into Slack. Secrets go in headers.

---

## 8. CORS — the "it works in curl but not in my browser" lesson

**The idea.** A browser will not let a page from one origin call a different
origin unless the second one says it is allowed.

**A picture.** A bouncer who works for the *visitor*, not the venue. Your
browser is protecting **its user** from a random web page quietly calling your
bank's API using their cookies.

**In the code.** `basics/files/static_and_cors.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],   # the Streamlit client
    ...
)
```

Different **port** means different **origin**. Streamlit on `:8501` calling
FastAPI on `:8000` is a cross-origin call, which is exactly why the capstone
needs this.

**Watch them trip.** They test with `curl`, it works, they conclude the API is
fine, and then the browser fails. Say: *"`curl` is not a browser and has no
bouncer. CORS is a browser rule, so only a browser enforces it."*

---

## 9. Testing — the pay-off for section 5

**The idea.** You can call your API in-process, with no server running and no
network. And because endpoints *ask* for their dependencies, tests can hand
them fakes.

**In the code.** `basics/testing/overriding_dependencies.py`:

```python
app.dependency_overrides[get_database] = fake_database
```

One line, and every endpoint that asked for a database now gets a dictionary
instead. No S3, no credentials, no waiting.

The file proves the override is doing something: one test runs *without* it
and asserts the route fails, so students can see the difference rather than
take it on faith.

**Say this:** *"This is why we did dependencies. Not to look clever — so that
the thing you cannot have in a test can be swapped for something you can."*

The project's own suite (`project/data_api/tests/test_api.py`) has **12 tests**
that never touch S3 and never train the model. They run in about a second.

**Watch them trip.** They forget to clean up the override, and it silently
changes the result of every test that runs afterwards. Every test in that file
uses `try/finally` for exactly this reason.

---

## 10. The capstone — where every lesson shows up

`fastapi/project/` is the same ideas in the arrangement real projects use.

### Walk them through one request

Trace `GET /datasets/iris?limit=5` out loud, in order. This single walkthrough
is worth more than another hour of slides:

1. **uvicorn** receives bytes on port 8000 and hands them to FastAPI
2. **CORS middleware** checks the origin (`main.py`)
3. **Routing** matches `/datasets/{name}` in `routers/datasets.py`
4. **Dependencies** resolve: `Pagination` reads `?limit=5`, `get_dataset` looks
   up `iris` — or raises 404 right here (`deps.py`)
5. **The endpoint function** finally runs, and slices a DataFrame
6. **The response model** (`Page` in `schemas.py`) checks and shapes the output
7. JSON goes back

Steps 2–6 are the entire course. Point at each one.

### And the map back to the lessons

| In the project | The lesson it came from |
| --- | --- |
| `schemas.py` | `models/` |
| `deps.py` — API key, pagination, dataset lookup | `structure/dependencies.py` |
| `routers/` — one file per resource | `structure/routers.py` |
| `config.py` | `structure/settings.py` |
| `lifespan` in `main.py` — train the model once | `async_work/` |
| `require_api_key` on `/model/predict` | `security/api_key.py` |
| the streaming CSV export | `files/download.py` |
| `tests/test_api.py` | `testing/` |

### The lifespan, in plain words

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    model.set_model(model.train())    # once, when the server starts
    yield                             # ... the server serves requests ...
    model.set_model(None)             # once, when it stops
```

Same `yield` shape as the dependency in section 5, one level up: setup, the
gap where everything happens, cleanup.

**Connect it to Streamlit**, since they know it:

| Streamlit | FastAPI |
| --- | --- |
| `@st.cache_resource` — load the model once | `lifespan` — train it at startup |
| `@st.cache_data` — do not redo slow work | `@lru_cache` in `store.py` |
| `st.session_state` | nothing — HTTP is stateless, which is *why* tokens exist |
| script re-runs top to bottom | one function per route, run on demand |

### The demo that makes the point

```bash
python fastapi/project/serve.py             # terminal 1 — the API
streamlit run fastapi/project/client.py     # terminal 2 — the front end
```

Then open `client.py` and ask the class to find the pandas. **There is none.**
No S3, no model, no CSV. It asks the API and draws the answer.

Then kill the API and refresh the page. It says *"The API is not running"*
instead of crashing — because someone thought about the failure.

Finish with: *"Two programs, one job each. Either can be rewritten without
touching the other. That is what an API buys you."*

---

## The ten things students get wrong

Keep this list next to you; most questions are on it.

1. Returning `{"error": ...}` with a 200 instead of raising `HTTPException`
2. Thinking type hints are decoration
3. `async def` with `time.sleep`, `requests`, or pandas inside
4. Sending a body with a GET request
5. Putting the API key in the URL instead of a header
6. Testing with curl, then being surprised the browser fails (CORS)
7. Loading the model inside the endpoint, so it reloads on every request
8. Writing validation by hand that Pydantic already does
9. Forgetting `response_model`, and leaking a field
10. Leaving a dependency override in place and poisoning later tests

---

## A three-session plan

**Session 1 — "an API is a function you can call over the network"**
`endpoints/` and `models/`. End with `response_model.py` and the password that
does not leak. *Homework: add an endpoint to `hello.py`.*

**Session 2 — "making it a real program"**
`errors/`, `structure/`, and the `async_work/` stopwatch demo. End with the
4.0s vs 1.0s comparison. *Homework: add a filter to a router.*

**Session 3 — "putting it together"**
`security/`, `testing/`, then the capstone. Trace one request end to end, run
both halves together, then kill the API to show the client handling it.
*Homework: add an endpoint to the Data API, with a test.*

---

## Glossary, in words a beginner can use

| Word | What it actually means |
| --- | --- |
| **Endpoint** | One URL your API answers, and the function behind it |
| **Route** | Same thing, said differently |
| **Path parameter** | A value taken from inside the URL: `/items/7` |
| **Query parameter** | A value after the `?`: `?limit=5` |
| **Body** | The JSON you send with POST or PUT |
| **Schema / model** | A class describing what data should look like |
| **Validation** | Checking data matches the schema — automatic here |
| **Dependency** | A small function that supplies something an endpoint needs |
| **Middleware** | Code that runs on every request, before and after |
| **Status code** | The number saying what happened: 200, 404, 500 |
| **Token** | Proof you logged in, sent with every later request |
| **CORS** | The browser rule about calling a different origin |
| **ASGI** | The plug between FastAPI and uvicorn. Do not dwell on it |
| **uvicorn** | The program that actually listens on the port |
| **OpenAPI** | The machine-readable description that builds `/docs` |

---

## One-sentence summaries, if you are short on time

- **Endpoints** — a URL plus a function; the signature says where values come from
- **Models** — describe data once, get validation and docs free
- **Errors** — raise, do not return; the status code is read first
- **Dependencies** — write shared setup once, and ask for it
- **Async** — `def` unless you `await`; concurrency is for overlapping waits
- **Security** — keys identify programs, tokens identify people
- **Testing** — swap the real world for a fake one, because you declared it
- **The project** — all of the above, with a Streamlit page that knows none of it
