"""
Concurrency -- doing several slow things at once instead of one after another.

What it shows:
    * asyncio.gather() to run awaitables together
    * the actual time saved, measured, not asserted
    * asyncio.to_thread() to use blocking code from an async endpoint safely
    * a timeout, so one slow dependency cannot hang the request forever

This is the pay-off for `async def`. One slow call gains nothing; five slow
calls that could overlap gain a lot.

Run it:
    python fastapi/basics/async_work/concurrency.py

Compare /sequential and /concurrent -- same work, very different clock time.
"""

import asyncio
import time

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Concurrency")


async def fetch_source(name: str, delay: float = 1.0) -> dict:
    """Stands in for a slow call to another service or database."""
    await asyncio.sleep(delay)
    return {"source": name, "rows": len(name) * 10}


SOURCES = ["orders", "customers", "products", "inventory"]


@app.get("/sequential")
async def sequential():
    """Await each one in turn: the delays add up."""
    started = time.perf_counter()
    results = [await fetch_source(name) for name in SOURCES]
    return {
        "results": results,
        "seconds": round(time.perf_counter() - started, 2),
        "note": "four 1-second calls, one after another",
    }


@app.get("/concurrent")
async def concurrent():
    """Start them all, then wait once: the delays overlap.

    gather() keeps the results in the order you passed them in, not the order
    they finished.
    """
    started = time.perf_counter()
    results = await asyncio.gather(*(fetch_source(name) for name in SOURCES))
    return {
        "results": results,
        "seconds": round(time.perf_counter() - started, 2),
        "note": "the same four calls, overlapping",
    }


def slow_blocking_work(n: int) -> int:
    """Ordinary blocking code -- pandas, scikit-learn, a normal DB driver."""
    time.sleep(1)
    return sum(range(n))


@app.get("/offloaded")
async def offloaded():
    """Calling blocking code from `async def`, without freezing the server.

    asyncio.to_thread moves it to a worker thread, so the event loop stays
    free. This is the escape hatch when you must be async but your library
    is not.
    """
    started = time.perf_counter()
    total = await asyncio.to_thread(slow_blocking_work, 1_000_000)
    return {"total": total, "seconds": round(time.perf_counter() - started, 2)}


@app.get("/with-timeout")
async def with_timeout(delay: float = 0.5):
    """Never wait forever on something you do not control.

    Try /with-timeout?delay=5 to see the 504.
    """
    try:
        result = await asyncio.wait_for(fetch_source("slow-service", delay), timeout=2.0)
    except asyncio.TimeoutError:
        raise HTTPException(504, "The upstream source took longer than 2 seconds")
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
