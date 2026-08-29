"""
Validation -- saying what "valid" means, and getting the errors for free.

What it shows:
    * Field() puts constraints on a model attribute (ranges, lengths, patterns)
    * @field_validator for rules a constraint cannot express
    * @model_validator for rules that involve more than one field
    * what a validation error actually looks like coming back

Every rule you add here is a rule you never write an `if` for in your endpoint,
and it documents itself in /docs at the same time.

Run it:
    python fastapi/basics/models/validation.py

Try POST /signup with a short password, or an age of 5, and read the 422.
"""

from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator

app = FastAPI(title="Validation")


class SignUp(BaseModel):
    username: str = Field(min_length=3, max_length=20,
                          description="3-20 characters")
    password: str = Field(min_length=8, description="At least 8 characters")
    password_confirm: str
    age: int = Field(ge=13, le=120, description="Must be at least 13")
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    @field_validator("username")
    @classmethod
    def no_spaces(cls, value: str) -> str:
        """One field, one rule that Field() cannot express."""
        if " " in value:
            raise ValueError("username cannot contain spaces")
        return value.lower()          # validators may also clean the value

    @model_validator(mode="after")
    def passwords_match(self):
        """Runs after every field is valid, so it can compare two of them."""
        if self.password != self.password_confirm:
            raise ValueError("passwords do not match")
        return self


class Booking(BaseModel):
    start: date
    end: date
    guests: int = Field(ge=1, le=10)

    @model_validator(mode="after")
    def end_after_start(self):
        if self.end <= self.start:
            raise ValueError("end date must be after start date")
        return self


@app.post("/signup")
def signup(data: SignUp):
    """If this function runs at all, `data` is valid. That is the whole point."""
    return {"created": data.username, "age": data.age}


@app.post("/bookings")
def book(booking: Booking):
    nights = (booking.end - booking.start).days
    return {"nights": nights, "guests": booking.guests}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
