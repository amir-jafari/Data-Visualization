"""Liveness and metadata. The first endpoint any deployment needs."""

from fastapi import APIRouter, Depends

from .. import model, store
from ..config import Settings, get_settings
from ..schemas import Health

router = APIRouter(tags=["health"])


@router.get("/health", response_model=Health)
def health(settings: Settings = Depends(get_settings)):
    """Cheap, unauthenticated, and honest about what is actually working.

    A health check that only returns {"status": "ok"} tells you nothing. This
    one reports whether the model loaded and whether S3 is reachable, which is
    what you actually want to know at 3am.
    """
    return Health(
        status="ok",
        version=settings.version,
        datasets=len(store.names()),
        model_ready=model.get_model() is not None,
        s3=store.s3_available(),
    )
