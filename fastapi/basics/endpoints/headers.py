"""
Headers and cookies -- the parts of a request the URL does not show.

What it shows:
    * Header() reads a request header; underscores map to hyphens for you
    * Cookie() reads a cookie the same way
    * the Request object, for when you want the raw details
    * setting a header or cookie on the way back out

Headers are where clients put things that are not really "data": who they are,
what format they want, and their credentials. The security chapter builds
directly on this.

Run it:
    python fastapi/basics/endpoints/headers.py

Try:
    curl -H "X-Token: abc123" http://127.0.0.1:8000/whoami
    curl -i http://127.0.0.1:8000/set-cookie
"""

from fastapi import Cookie, FastAPI, Header, Request, Response

app = FastAPI(title="Headers and cookies")


@app.get("/whoami")
def whoami(
    user_agent: str | None = Header(default=None),
    x_token: str | None = Header(default=None),
):
    """Note the names.

    `user_agent` reads the `User-Agent` header and `x_token` reads `X-Token`:
    Python cannot have a hyphen in an identifier, so FastAPI converts
    underscores to hyphens automatically.
    """
    return {"user_agent": user_agent, "x_token": x_token}


@app.get("/preferences")
def preferences(theme: str | None = Cookie(default=None)):
    """Cookies are read exactly like headers, because that is what they are."""
    return {"theme": theme or "not set -- call /set-cookie first"}


@app.get("/set-cookie")
def set_cookie(response: Response):
    """Ask for a Response object and you can set headers and cookies on it.

    Use `curl -i` to see them; a browser hides this.
    """
    response.set_cookie(key="theme", value="dark")
    response.headers["X-Course"] = "data-visualization"
    return {"message": "cookie and header set -- now call /preferences"}


@app.get("/raw")
def raw_request(request: Request):
    """The escape hatch: the whole request, when the shortcuts are not enough.

    Reach for this rarely -- the typed parameters above are self-documenting
    and validated, and `request` is neither.
    """
    return {
        "method": request.method,
        "url": str(request.url),
        "client": request.client.host if request.client else None,
        "headers": dict(request.headers),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
