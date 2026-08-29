"""
Query parameters -- the `?key=value` part of a URL.

What it shows:
    * a function argument that is NOT in the path becomes a query parameter
    * a default value makes it optional; no default makes it required
    * `| None` is how you say "optional, and there is no sensible default"
    * Query() adds validation and documentation, exactly like Path() did
    * the same name repeated becomes a list

Run it:
    python fastapi/basics/endpoints/query_params.py

Try:
    /search?q=python
    /search?q=python&limit=5&offset=10
    /search                            -> 422: q is required
    /filter?tag=red&tag=blue           -> a list of two tags
"""

from fastapi import FastAPI, Query

app = FastAPI(title="Query parameters")

ITEMS = [{"id": i, "name": f"item-{i}"} for i in range(1, 51)]


@app.get("/search")
def search(
    q: str,                 # no default -> required
    limit: int = 10,        # has a default -> optional
    offset: int = 0,
):
    """The classic trio: a search term, and how much of the result to return.

    Nothing here says "query parameter". FastAPI works it out: `q` is not in
    the path, so it must come from the query string.
    """
    hits = [item for item in ITEMS if q in item["name"]]
    return {
        "query": q,
        "total": len(hits),
        "items": hits[offset:offset + limit],
    }


@app.get("/optional")
def optional_param(category: str | None = None):
    """`str | None = None` means "you may leave this out entirely".

    Without the `| None`, a default of None would still be typed as a string
    and FastAPI would try to validate None as one.
    """
    if category is None:
        return {"message": "no category given -- showing everything"}
    return {"category": category}


@app.get("/validated")
def validated(
    q: str = Query(min_length=3, max_length=20, description="At least 3 characters"),
    page: int = Query(1, ge=1, description="Page number, starting at 1"),
):
    """Rules on the value, not just the type. Try /validated?q=ab"""
    return {"q": q, "page": page}


@app.get("/filter")
def filter_by_tags(tag: list[str] = Query(default=[])):
    """Repeat the parameter to build a list: /filter?tag=red&tag=blue"""
    return {"tags": tag, "count": len(tag)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
