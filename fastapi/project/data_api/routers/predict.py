"""Serving the model. The route that needs a key, because it costs something."""

from fastapi import APIRouter, Depends, HTTPException, status

from .. import model as model_module
from ..deps import require_api_key
from ..schemas import ModelInfo, PredictResponse, Prediction

router = APIRouter(prefix="/model", tags=["model"])


def loaded_model() -> model_module.TrainedModel:
    """503, not 500: the service is fine, it is just not ready yet."""
    trained = model_module.get_model()
    if trained is None:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "The model is not loaded. Check /health.",
        )
    return trained


@router.get("/info", response_model=ModelInfo)
def model_info(trained: model_module.TrainedModel = Depends(loaded_model)):
    """What the model expects. Call this before /predict to get the feature names."""
    return ModelInfo(
        model_name=type(trained.estimator).__name__,
        trained_on=trained.trained_on,
        n_features=len(trained.features),
        features=trained.features,
        target_names=trained.target_names,
        test_accuracy=round(trained.accuracy, 4),
    )


@router.post("/predict", response_model=PredictResponse,
             dependencies=[Depends(require_api_key)])
def predict(
    request: "PredictRequest",
    trained: model_module.TrainedModel = Depends(loaded_model),
):
    """Predict for a batch of rows.

    Batching is not a nicety: one request with 500 rows is far cheaper than
    500 requests, and the size cap on `rows` is what stops a caller using it
    to exhaust the server.
    """
    results = trained.predict(request.rows)
    return PredictResponse(
        model_name=type(trained.estimator).__name__,
        target_names=trained.target_names,
        predictions=[Prediction(prediction=label, confidence=round(score, 4))
                     for label, score in results],
    )


from ..schemas import PredictRequest  # noqa: E402  (resolves the annotation above)
