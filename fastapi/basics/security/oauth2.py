"""
OAuth2 password flow -- real user logins, with tokens.

What it shows:
    * POST /token exchanges a username and password for an access token
    * OAuth2PasswordBearer reads "Authorization: Bearer <token>" from then on
    * hashing passwords, so a leaked database is not a leaked password list
    * the "Authorize" button in /docs, wired up for free
    * scopes, to say what a token is allowed to do

The name is intimidating; the flow is not. Log in once, get a token, send the
token with every later request.

This lesson uses a signed, expiring token built from the standard library, so
there is nothing extra to install. A real project would use `python-jose` or
`pyjwt` for proper JWTs -- the shape is identical.

Run it:
    python fastapi/basics/security/oauth2.py

In /docs click "Authorize" and log in as ada / secret.
"""

import base64
import hashlib
import hmac
import json
import time

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI(title="OAuth2 password flow")

SECRET = "change-me-in-real-life"
TOKEN_TTL_SECONDS = 30 * 60


def hash_password(password: str, salt: str = "course-salt") -> str:
    """Never store a password. Store something you can only check against.

    Real projects use bcrypt or argon2, which are deliberately slow. sha256 is
    used here only to keep the dependency list empty.
    """
    return hashlib.sha256((salt + password).encode()).hexdigest()


USERS = {
    "ada": {"password_hash": hash_password("secret"), "scopes": ["read", "write"]},
    "bob": {"password_hash": hash_password("hunter2"), "scopes": ["read"]},
}

# tokenUrl tells /docs where the login endpoint is, so "Authorize" works.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(username: str, scopes: list[str]) -> str:
    """A payload plus a signature, so the server can detect tampering."""
    payload = {"sub": username, "scopes": scopes, "exp": time.time() + TOKEN_TTL_SECONDS}
    body = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    signature = hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{signature}"


def decode_token(token: str) -> dict:
    """Check the signature first, then the expiry. Never trust the payload."""
    try:
        body, signature = token.split(".")
        expected = hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError("bad signature")
        payload = json.loads(base64.urlsafe_b64decode(body))
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token",
                            headers={"WWW-Authenticate": "Bearer"})

    if payload["exp"] < time.time():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token has expired",
                            headers={"WWW-Authenticate": "Bearer"})
    return payload


@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    """The login endpoint.

    OAuth2PasswordRequestForm reads `username` and `password` as form fields --
    that is what the spec requires, and what the /docs Authorize dialog sends.
    """
    user = USERS.get(form.username)
    if user is None or not hmac.compare_digest(
        user["password_hash"], hash_password(form.password)
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong username or password")

    return {
        "access_token": create_token(form.username, user["scopes"]),
        "token_type": "bearer",
    }


def current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Every protected route depends on this, directly or indirectly."""
    return decode_token(token)


def require_write(user: dict = Depends(current_user)) -> dict:
    """Scopes: not just "who are you" but "what may you do"."""
    if "write" not in user["scopes"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This token cannot write")
    return user


@app.get("/me")
def read_me(user: dict = Depends(current_user)):
    return {"username": user["sub"], "scopes": user["scopes"]}


@app.post("/items")
def create_item(name: str, user: dict = Depends(require_write)):
    """ada can do this. bob has a read-only token and gets a 403."""
    return {"created": name, "by": user["sub"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
