"""Where the data comes from.

Two sources, in order of preference:

  1. the course S3 bucket, if credentials are available
  2. datasets bundled with scikit-learn, so the API always works

Everything is cached in memory after the first read -- an API that re-downloads
a CSV on every request is not an API, it is a denial of service against itself.
"""

import io
from functools import lru_cache

import pandas as pd

from .config import aws_credentials, get_settings


# --- built-in fallback -----------------------------------------------------
@lru_cache
def _builtin() -> dict[str, pd.DataFrame]:
    """scikit-learn ships these, so they need no network and no keys."""
    from sklearn.datasets import load_breast_cancer, load_diabetes, load_iris

    frames = {}
    for name, loader in (("iris", load_iris),
                         ("breast_cancer", load_breast_cancer),
                         ("diabetes", load_diabetes)):
        bunch = loader(as_frame=True)
        frame = bunch.frame.copy()
        # Turn the numeric target into readable labels where we have names.
        if hasattr(bunch, "target_names") and bunch.target_names is not None:
            try:
                frame["target"] = [bunch.target_names[i] for i in bunch.target]
            except (IndexError, TypeError):
                pass
        frames[name] = frame
    return frames


# --- S3 --------------------------------------------------------------------
@lru_cache
def _s3_client():
    """None if we have no credentials -- callers treat that as "no S3"."""
    credentials = aws_credentials()
    if not credentials:
        return None
    try:
        import boto3
        return boto3.Session(
            aws_access_key_id=credentials.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=credentials.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=credentials.get("AWS_SESSION_TOKEN"),
        ).client("s3", region_name=credentials.get("AWS_DEFAULT_REGION", "us-east-1"))
    except Exception:
        return None


@lru_cache
def _s3_catalog() -> dict[str, str]:
    """{dataset name: S3 key} for every CSV under the configured prefix."""
    client = _s3_client()
    if client is None:
        return {}

    settings = get_settings()
    catalog = {}
    try:
        pages = client.get_paginator("list_objects_v2").paginate(
            Bucket=settings.s3_bucket, Prefix=settings.s3_prefix)
        for page in pages:
            for obj in page.get("Contents", []):
                key = obj["Key"]
                if key.lower().endswith(".csv"):
                    name = key.rsplit("/", 1)[-1].removesuffix(".csv")
                    catalog[name] = key
    except Exception:
        # Expired keys are the normal case on a teaching account. Degrade to
        # the built-in datasets rather than failing every request.
        return {}
    return catalog


@lru_cache
def _from_s3(name: str) -> pd.DataFrame | None:
    key = _s3_catalog().get(name)
    client = _s3_client()
    if key is None or client is None:
        return None
    try:
        body = client.get_object(Bucket=get_settings().s3_bucket, Key=key)["Body"].read()
        frame = pd.read_csv(io.BytesIO(body))
        return frame.dropna(axis=1, how="all")   # drop trailing-comma phantom columns
    except Exception:
        return None


# --- the public interface --------------------------------------------------
def s3_available() -> bool:
    return bool(_s3_catalog())


def names() -> list[str]:
    return sorted(set(_builtin()) | set(_s3_catalog()))


def source_of(name: str) -> str:
    return "s3" if name in _s3_catalog() else "built-in"


def load(name: str) -> pd.DataFrame | None:
    """The dataset, or None if there is no such name. S3 wins over built-in."""
    frame = _from_s3(name)
    if frame is not None:
        return frame
    frame = _builtin().get(name)
    return frame.copy() if frame is not None else None


def reset_cache() -> None:
    """Forget everything -- used by tests, and after credentials change."""
    for cached in (_builtin, _s3_client, _s3_catalog, _from_s3):
        cached.cache_clear()
