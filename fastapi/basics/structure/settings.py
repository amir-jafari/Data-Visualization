"""
Settings -- configuration that is not hard-coded.

What it shows:
    * pydantic-settings reads environment variables into a typed object
    * a .env file for local development
    * @lru_cache so the settings are built once, not per request
    * settings as a dependency, which is what makes them swappable in tests

The rule this enforces: no secrets, hostnames or ports written into source
code. The same image runs in development and production, and only the
environment changes.

Run it:
    python fastapi/basics/structure/settings.py
    APP_NAME="My API" DEBUG=true python fastapi/basics/structure/settings.py
"""

from functools import lru_cache

from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Every field can be set by an environment variable of the same name.

    Types are enforced: DEBUG=maybe is rejected at startup, not at 3am.
    """

    app_name: str = "Data API"
    debug: bool = False
    page_size: int = 25
    api_key: str = "dev-key-change-me"
    database_url: str = "sqlite:///./app.db"

    model_config = SettingsConfigDict(
        env_file=".env",          # read this file if it exists
        env_file_encoding="utf-8",
        extra="ignore",           # ignore unrelated variables in the environment
    )


@lru_cache
def get_settings() -> Settings:
    """Built once and reused.

    Without the cache, every request would re-read the environment and the
    .env file. With it, and because it is a dependency, a test can replace
    the whole object -- see the testing chapter.
    """
    return Settings()


app = FastAPI(title="Settings")


@app.get("/config")
def show_config(settings: Settings = Depends(get_settings)):
    """Note what is NOT returned. Never echo a secret back out."""
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "page_size": settings.page_size,
        "api_key_set": settings.api_key != "dev-key-change-me",
    }


@app.get("/items")
def list_items(settings: Settings = Depends(get_settings)):
    """A real use: the page size comes from configuration, not from a literal."""
    return {"returned": settings.page_size}


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    print(f"Starting {settings.app_name!r} (debug={settings.debug})")
    uvicorn.run(app, host="127.0.0.1", port=8000)
