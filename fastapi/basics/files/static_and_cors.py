"""
Static files and CORS -- serving a front end, and letting one call you.

What it shows:
    * app.mount() to serve a folder of files (HTML, CSS, JS, images)
    * CORSMiddleware, and what problem it actually solves
    * why the browser blocks cross-origin calls but curl never does
    * mount order: mounting "/" last, so it does not swallow your API routes

CORS is the single most common "it works in curl but not in my browser"
problem. The rule: a page served from origin A may not call origin B unless B
says it is allowed. Your API is B, and CORSMiddleware is how it says so.

Run it:
    python fastapi/basics/files/static_and_cors.py

Open http://127.0.0.1:8000/ and run the fetch() from the page.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Static files and CORS")

HERE = Path(__file__).resolve().parent

# --- CORS -----------------------------------------------------------------
# Only these origins may call this API from a browser page. A Streamlit app on
# port 8501 is exactly the case this course needs: different port means
# different origin, so without this the browser blocks the call.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",     # Streamlit
        "http://127.0.0.1:8501",
        "http://localhost:3000",     # a typical React dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# allow_origins=["*"] works but is a blunt instrument -- and it is incompatible
# with allow_credentials=True, which browsers refuse to honour on a wildcard.


# --- API routes, declared BEFORE the mount --------------------------------
@app.get("/api/hello")
def hello():
    return {"message": "hello from the API"}


@app.get("/api/data")
def data():
    return {"rows": [{"x": i, "y": i * i} for i in range(10)]}


# --- static files, mounted LAST -------------------------------------------
# A mount at "/" matches everything underneath it, so anything mounted here
# before the routes above would shadow them. Mount last, or use a prefix.
app.mount("/", StaticFiles(directory=HERE / "static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
