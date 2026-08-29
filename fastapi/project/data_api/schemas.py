"""Every shape this API accepts or returns, in one place.

Keeping them together is deliberate: this file *is* the API's contract, and
it is what /docs shows to whoever has to call it.
"""

from typing import Any, Literal

from pydantic import BaseModel, Field


class DatasetInfo(BaseModel):
    """One entry in the catalogue."""
    name: str
    rows: int
    columns: list[str]
    source: Literal["s3", "built-in"]


class Page(BaseModel):
    """A page of rows, plus enough information to ask for the next one."""
    dataset: str
    total: int = Field(description="Rows matching the filter, before paging")
    limit: int
    offset: int
    returned: int
    rows: list[dict[str, Any]]


class ColumnSummary(BaseModel):
    column: str
    dtype: str
    missing: int
    unique: int
    mean: float | None = None
    std: float | None = None
    min: float | None = None
    max: float | None = None


class DatasetSummary(BaseModel):
    dataset: str
    rows: int
    columns: list[ColumnSummary]


class PredictRequest(BaseModel):
    """Features for one or more rows.

    A dict per row keeps this readable in /docs and forgiving about column
    order -- the model is asked for the columns it was trained on, by name.
    """
    rows: list[dict[str, float]] = Field(min_length=1, max_length=1000)

    model_config = {
        "json_schema_extra": {
            "example": {"rows": [{"mean radius": 14.1, "mean texture": 20.2}]}
        }
    }


class Prediction(BaseModel):
    prediction: str
    confidence: float = Field(ge=0, le=1)


class PredictResponse(BaseModel):
    model_name: str
    target_names: list[str]
    predictions: list[Prediction]


class ModelInfo(BaseModel):
    model_name: str
    trained_on: str
    n_features: int
    features: list[str]
    target_names: list[str]
    test_accuracy: float


class Health(BaseModel):
    status: Literal["ok"]
    version: str
    datasets: int
    model_ready: bool
    s3: bool
