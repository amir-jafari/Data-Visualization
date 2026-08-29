"""
Nested models -- describing data that is not flat.

What it shows:
    * a model can contain another model, and lists of them
    * validation goes all the way down, and errors point at the exact field
    * `Literal` and `Enum` for "one of these values only"
    * a worked example of the shape real APIs actually return

Run it:
    python fastapi/basics/models/nested_models.py

POST /orders from /docs, then break one line of the nested JSON and look at
where the error message points.
"""

from enum import Enum
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Nested models")


class Status(str, Enum):
    """Inheriting from str as well as Enum keeps it JSON-friendly."""
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"


class Address(BaseModel):
    street: str
    city: str
    country: str = Field(min_length=2, max_length=2, description="Two-letter code")


class OrderLine(BaseModel):
    product: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(gt=0)

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


class Order(BaseModel):
    """A model made of other models -- the normal case, once data is real."""
    customer: str
    shipping: Address                       # one nested model
    lines: list[OrderLine] = Field(min_length=1)   # a list of them
    status: Status = Status.pending
    priority: Literal["standard", "express"] = "standard"


@app.post("/orders")
def create_order(order: Order):
    """Validation reached every line of every nested object before this ran."""
    total = sum(line.total for line in order.lines)
    return {
        "customer": order.customer,
        "city": order.shipping.city,
        "line_count": len(order.lines),
        "total": round(total, 2),
        "status": order.status,
    }


@app.get("/orders/example", response_model=Order)
def example_order():
    """A ready-made example, so you can copy the shape into POST /orders."""
    return Order(
        customer="Ada Lovelace",
        shipping=Address(street="1 Analytical Way", city="London", country="GB"),
        lines=[OrderLine(product="Punch cards", quantity=100, unit_price=0.5)],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
