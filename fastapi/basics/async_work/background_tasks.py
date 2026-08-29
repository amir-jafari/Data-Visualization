"""
Background tasks -- answering now, finishing the work afterwards.

What it shows:
    * BackgroundTasks runs a function *after* the response is sent
    * the client is not kept waiting for slow follow-up work
    * tasks can be added from a dependency as well as an endpoint
    * where the limits are, and when you need a real queue instead

Typical use: send the confirmation email, write the audit log, invalidate a
cache. Things that must happen, but that the caller should not wait for.

Run it:
    python fastapi/basics/async_work/background_tasks.py

POST /signup, notice the instant reply, then GET /log a second later and see
the work that happened after you were answered.
"""

import time

from fastapi import BackgroundTasks, Depends, FastAPI
from pydantic import BaseModel

app = FastAPI(title="Background tasks")

LOG: list[str] = []


class User(BaseModel):
    username: str
    email: str


def send_welcome_email(email: str):
    """Pretend this talks to a mail server and takes two seconds."""
    time.sleep(2)
    LOG.append(f"{time.strftime('%H:%M:%S')} sent welcome email to {email}")


def write_audit(action: str, who: str):
    LOG.append(f"{time.strftime('%H:%M:%S')} audit: {action} by {who}")


@app.post("/signup")
def signup(user: User, background: BackgroundTasks):
    """Ask for a BackgroundTasks parameter and add work to it.

    The response goes out immediately; the two tasks run afterwards, in the
    order they were added.
    """
    background.add_task(write_audit, "signup", user.username)
    background.add_task(send_welcome_email, user.email)

    return {"created": user.username, "note": "email is being sent in the background"}


def audit_dependency(background: BackgroundTasks):
    """Dependencies can queue background work too.

    Handy for cross-cutting concerns: every route that uses this gets logged
    without mentioning it.
    """
    background.add_task(write_audit, "request", "dependency")
    return True


@app.get("/audited", dependencies=[Depends(audit_dependency)])
def audited():
    return {"message": "this call was logged from a dependency"}


@app.get("/log")
def read_log():
    """Call this a couple of seconds after /signup to see the work land.

    Worth knowing when you get to the testing chapter: TestClient runs
    background tasks *before* it returns, so a test will not see the instant
    reply that a real client gets. Measured against a real server, POST
    /signup answers in about 5 milliseconds and the email lands 2 seconds
    later; under TestClient the same call appears to take the full 2 seconds.
    """
    return {"entries": LOG}


@app.get("/limits")
def limits():
    """BackgroundTasks is deliberately simple. Know when to outgrow it."""
    return {
        "good for": "short work that may fail quietly -- emails, logs, cache busting",
        "not good for": "anything that must survive a restart, be retried, or "
                        "take minutes",
        "because": "the task runs inside this server process, with no queue, "
                   "no retries and no persistence",
        "next step": "Celery, RQ, or arq with Redis",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
