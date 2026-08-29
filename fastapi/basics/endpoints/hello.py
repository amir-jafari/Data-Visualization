"""
Hello, FastAPI -- the smallest API that does something.

What it shows:
    * an "app" is just an object; a route is a function with a decorator on it
    * the decorator says *which URL* and *which HTTP verb* the function answers
    * whatever you return is turned into JSON for you
    * you get interactive documentation for free, without writing any

Run it:
    python fastapi/basics/endpoints/hello.py

Then open two things in your browser:
    http://127.0.0.1:8000/          <- the endpoint itself
    http://127.0.0.1:8000/docs      <- documentation FastAPI generated for you

The /docs page is the thing to notice. It is not a static page someone wrote --
FastAPI built it by reading your function signatures. Every lesson in this
course has one, and you can call your endpoints from it without a browser
plugin, curl, or Postman.
"""

from fastapi import FastAPI

# title and description show up at the top of /docs.
app = FastAPI(
    title="Hello API",
    description="The smallest FastAPI app there is.",
)


@app.get("/")
def read_root():
    """Answer GET requests to `/`.

    The docstring you are reading becomes the endpoint's description in /docs.
    """
    # Return a dict. FastAPI serialises it to JSON and sets the content type.
    return {"message": "Hello, FastAPI"}


@app.get("/ping")
def ping():
    """A second route, so you can see that the path is what tells them apart."""
    return {"status": "alive"}


if __name__ == "__main__":
    import uvicorn

    # uvicorn is the web server that actually listens on the port. FastAPI
    # only describes *what* to answer; uvicorn does the answering.
    uvicorn.run(app, host="127.0.0.1", port=8000)
