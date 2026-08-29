"""
API keys -- the simplest authentication that is worth using.

What it shows:
    * reading a key from a header with FastAPI's APIKeyHeader
    * turning it into a dependency, so routes just declare "I need a key"
    * a padlock button in /docs, so you can try protected routes there
    * comparing secrets with compare_digest instead of ==

An API key says *which caller* this is. It does not say who the human is. That
is fine for service-to-service calls and course projects; use the OAuth2
lesson next door when there are real user accounts.

Run it:
    python fastapi/basics/security/api_key.py
    curl -H "X-API-Key: student-key" http://127.0.0.1:8000/data
"""

from hmac import compare_digest

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader

app = FastAPI(title="API keys")

# In a real app these come from settings/a database, never from source.
KEYS = {"student-key": "student", "admin-key": "admin"}

# The scheme object does two jobs: it reads the header, and it tells /docs
# that this API uses a key, which is what draws the padlock button.
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_key(key: str = Depends(api_key_header)) -> str:
    """Turn a raw header into a caller, or refuse the request."""
    if key is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Missing X-API-Key header",
        )

    # compare_digest takes the same time whichever character differs, so an
    # attacker cannot guess a key one character at a time by timing replies.
    for known, role in KEYS.items():
        if compare_digest(key, known):
            return role

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API key")


def require_admin(role: str = Depends(require_key)) -> str:
    """Dependencies stack: this one needs a valid key *and* the admin role."""
    if role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin key required")
    return role


@app.get("/public")
def public():
    """No dependency, no key needed."""
    return {"message": "anyone can read this"}


@app.get("/data")
def read_data(role: str = Depends(require_key)):
    """One line is all it takes to protect a route."""
    return {"role": role, "rows": [1, 2, 3]}


@app.delete("/data")
def delete_data(role: str = Depends(require_admin)):
    return {"deleted": True, "by": role}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
