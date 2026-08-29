"""Settings for the Data API, from the environment or a .env file."""

import importlib.util
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "Course Data API"
    version: str = "1.0.0"
    api_key: str = "student-key"
    page_size: int = 50
    max_page_size: int = 500

    # S3 is optional. Without it the API serves its built-in datasets instead,
    # so the whole project runs with no credentials at all.
    s3_bucket: str = "dats-dl"
    s3_prefix: str = "ajafari@gwu.edu/streamlit/data/"

    allowed_origins: list[str] = [
        "http://localhost:8501", "http://127.0.0.1:8501",   # Streamlit
    ]

    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / "fastapi" / ".env",
        env_prefix="API_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Built once. As a dependency, a test can replace the whole object."""
    return Settings()


@lru_cache
def aws_credentials() -> dict:
    """Borrow the [s3] block from the Streamlit course's credentials file.

    One .env for the repo beats two copies of the same expiring keys. If that
    file (or its reader) is missing, we return nothing and the API falls back
    to its built-in datasets -- so this never becomes a hard requirement.
    """
    reader = REPO_ROOT / "streamlit" / "env_config.py"
    if not reader.is_file():
        return {}

    try:
        spec = importlib.util.spec_from_file_location("_course_env", reader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.as_boto_env("s3")
    except Exception:
        return {}
