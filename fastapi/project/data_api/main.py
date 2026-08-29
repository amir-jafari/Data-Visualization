"""
The Course Data API -- everything from basics/, assembled into one service.

What it does:
    * serves the course datasets from S3, falling back to built-in ones
    * pages, filters, sorts and exports them
    * serves predictions from a model trained once at startup
    * protects the expensive route with an API key

Which lesson each piece came from:
    endpoints/      path and query parameters on every route
    models/         schemas.py -- one description of every shape
    errors/         a domain exception turned into a clean 404/422
    structure/      routers/, deps.py, config.py
    async_work/     lifespan, so the model trains once and not per request
    security/       deps.require_api_key on /model/predict
    files/          the streaming CSV export, and CORS for the Streamlit client
    testing/        tests/test_api.py, using dependency overrides

Run it (from the repo root):
    python fastapi/project/serve.py

    ...or directly, which is the same thing:
    uvicorn data_api.main:app --reload --app-dir fastapi/project

Note you cannot run this file itself -- `from . import store` needs the code
to be imported as a package, which is exactly what serve.py arranges.

Then:
    http://127.0.0.1:8000/docs      the interactive documentation
    python fastapi/project/client.py   the Streamlit front end (separate terminal)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import model, store
from .config import get_settings
from .routers import datasets, health, predict


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown, in one function.

    Everything before `yield` runs once when the server starts; everything
    after runs once when it stops. Training the model here -- rather than on
    first request -- means the first user does not pay for it, and /health can
    honestly report whether the service is ready.
    """
    try:
        model.set_model(model.train())
    except Exception as exc:                      # noqa: BLE001
        # A failed model should not stop the data endpoints from working.
        # /health will report model_ready: false, and /model/* returns 503.
        print(f"[startup] model training failed: {exc}")
        model.set_model(None)

    yield

    model.set_model(None)
    store.reset_cache()


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan,
    description=(
        "Datasets and predictions for the Data Visualization course.\n\n"
        "Most routes are open. `/model/predict` needs an `X-API-Key` header."
    ),
)

# The Streamlit client runs on a different port, which makes it a different
# origin as far as the browser is concerned. Without this it cannot call us.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(datasets.router)
app.include_router(predict.router)


@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception):
    """Never show a traceback to a caller."""
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "message": "Something went wrong."},
    )


@app.get("/", tags=["health"])
def root():
    """A signpost, so a browser hitting the root is not just told 404."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "docs": "/docs",
        "endpoints": ["/health", "/datasets", "/model/info", "/model/predict"],
    }
