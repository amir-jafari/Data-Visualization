"""
def or async def -- the choice people get wrong, and why it matters.

The short version:

    def         -> FastAPI runs it in a worker thread. Blocking is fine here.
    async def   -> runs on the event loop. Blocking here freezes the WHOLE
                   server for every user, not just this request.

So the dangerous combination is `async def` plus code that blocks: time.sleep,
requests.get, a normal database driver, a long CPU loop. If you are not going
to `await` something, use a plain `def` and let FastAPI handle the threading.

What it shows:
    * three versions of the same slow endpoint, two good and one harmful
    * why "async" is not automatically faster
    * the rule of thumb, at the bottom of this file

Run it:
    python fastapi/basics/async_work/sync_vs_async.py

Then, in two terminals at once:
    curl http://127.0.0.1:8000/blocking-async     # start this first
    curl http://127.0.0.1:8000/quick              # ...this waits for it

Do the same with /blocking-sync and /quick answers immediately.
"""

import asyncio
import time

from fastapi import FastAPI

app = FastAPI(title="def vs async def")


@app.get("/quick")
def quick():
    """A fast endpoint, used to see whether the server is still responsive."""
    return {"message": "instant"}


@app.get("/blocking-sync")
def blocking_sync():
    """GOOD. A plain `def`, so FastAPI runs it in a thread pool.

    time.sleep blocks this thread, but the event loop is untouched and other
    requests are served normally.
    """
    started = time.perf_counter()
    time.sleep(3)                       # stands in for a slow library call
    return {"style": "def + blocking call", "seconds": round(time.perf_counter() - started, 1)}


@app.get("/blocking-async")
async def blocking_async():
    """BAD. `async def` with a blocking call inside.

    Nothing is awaited, so the event loop cannot switch to another task. Every
    other request queues behind this one. This is the mistake to remember.
    """
    started = time.perf_counter()
    time.sleep(3)                       # blocks the entire event loop
    return {"style": "async def + blocking call (harmful)",
            "seconds": round(time.perf_counter() - started, 1)}


@app.get("/awaiting-async")
async def awaiting_async():
    """GOOD. `async def` with something genuinely awaitable.

    `await` hands control back to the event loop, which serves other requests
    while this one waits.
    """
    started = time.perf_counter()
    await asyncio.sleep(3)
    return {"style": "async def + await", "seconds": round(time.perf_counter() - started, 1)}


@app.get("/rule")
def rule_of_thumb():
    return {
        "use async def": "only when the body actually awaits something "
                         "(httpx, asyncpg, aiofiles, asyncio.sleep)",
        "use def": "for everything else -- pandas, scikit-learn, requests, "
                   "a normal DB driver, plain CPU work",
        "never": "async def with a blocking call inside",
        "why": "def runs in a thread pool; async def runs on the shared event loop",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
