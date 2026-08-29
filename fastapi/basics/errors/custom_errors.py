"""
Custom error handling -- one consistent error shape for the whole API.

What it shows:
    * @app.exception_handler() to catch your own exception classes
    * overriding FastAPI's validation error, to reshape 422 responses
    * a catch-all handler, so an unexpected bug does not leak a traceback
    * why a domain exception beats raising HTTPException deep in your code

The pattern: business logic raises a *domain* error that knows nothing about
HTTP; a handler at the edge turns it into a response. Your logic stays testable
without a web server, and every error looks the same to the client.

Run it:
    python fastapi/basics/errors/custom_errors.py

Try /accounts/1/withdraw?amount=999999 and /boom
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Custom errors")


# --- domain exceptions: no mention of HTTP anywhere ------------------------
class InsufficientFunds(Exception):
    def __init__(self, balance: float, requested: float):
        self.balance = balance
        self.requested = requested


class AccountNotFound(Exception):
    def __init__(self, account_id: int):
        self.account_id = account_id


ACCOUNTS = {1: 250.0, 2: 40.0}


# --- handlers: the only place that knows about status codes ---------------
@app.exception_handler(InsufficientFunds)
def handle_insufficient_funds(request: Request, exc: InsufficientFunds):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "insufficient_funds",
            "message": f"Balance is {exc.balance}, cannot withdraw {exc.requested}",
            "short_by": round(exc.requested - exc.balance, 2),
        },
    )


@app.exception_handler(AccountNotFound)
def handle_account_not_found(request: Request, exc: AccountNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "account_not_found", "account_id": exc.account_id},
    )


@app.exception_handler(RequestValidationError)
def handle_validation_error(request: Request, exc: RequestValidationError):
    """Reshape FastAPI's own 422 so it matches the errors above.

    The default 422 body is good, but it looks nothing like your other errors.
    Clients appreciate one shape.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_failed",
            "fields": [
                {"field": ".".join(str(p) for p in err["loc"][1:]), "problem": err["msg"]}
                for err in exc.errors()
            ],
        },
    )


@app.exception_handler(Exception)
def handle_everything_else(request: Request, exc: Exception):
    """The safety net. Without it, an unhandled bug returns a stack trace.

    Log the real error server-side; tell the client only that it failed.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "internal_error", "message": "Something went wrong."},
    )


# --- the endpoints, which stay clean --------------------------------------
@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: int, amount: float):
    """Note there is no error formatting in here at all."""
    if account_id not in ACCOUNTS:
        raise AccountNotFound(account_id)

    balance = ACCOUNTS[account_id]
    if amount > balance:
        raise InsufficientFunds(balance, amount)

    ACCOUNTS[account_id] = balance - amount
    return {"account_id": account_id, "withdrew": amount, "balance": ACCOUNTS[account_id]}


@app.get("/boom")
def boom():
    """A deliberate bug, to show the catch-all handler working."""
    return 1 / 0


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
