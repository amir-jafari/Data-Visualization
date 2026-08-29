"""The prediction model: trained once at startup, then reused.

This is the @st.cache_resource idea from the Streamlit course, in its FastAPI
form -- a module-level object built during the app's lifespan, not per request.
"""

from dataclasses import dataclass

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from . import store

TRAINING_DATASET = "breast_cancer"


@dataclass
class TrainedModel:
    estimator: RandomForestClassifier
    features: list[str]
    target_names: list[str]
    accuracy: float
    trained_on: str

    def predict(self, rows: list[dict[str, float]]) -> list[tuple[str, float]]:
        """Predict, tolerating missing or out-of-order columns.

        Callers send JSON objects, so column order means nothing. Reindexing by
        name puts them right, and fills anything absent with 0 rather than
        failing -- a deliberate trade-off for a teaching API, and one worth
        knowing you have made.
        """
        frame = pd.DataFrame(rows).reindex(columns=self.features, fill_value=0.0)
        probabilities = self.estimator.predict_proba(frame)

        results = []
        for row in probabilities:
            best = int(row.argmax())
            results.append((str(self.target_names[best]), float(row[best])))
        return results


_model: TrainedModel | None = None


def train() -> TrainedModel:
    """Fit the model. Called once, from the app's lifespan handler."""
    frame = store.load(TRAINING_DATASET)
    if frame is None:
        raise RuntimeError(f"Cannot train: dataset {TRAINING_DATASET!r} is unavailable")

    target = "target" if "target" in frame else frame.columns[-1]
    features = [c for c in frame.select_dtypes("number").columns if c != target]

    X = frame[features]
    y = frame[target].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)

    estimator = RandomForestClassifier(n_estimators=100, random_state=42)
    estimator.fit(X_train, y_train)

    return TrainedModel(
        estimator=estimator,
        features=features,
        target_names=sorted(y.unique()),
        accuracy=float(estimator.score(X_test, y_test)),
        trained_on=TRAINING_DATASET,
    )


def set_model(model: TrainedModel | None) -> None:
    global _model
    _model = model


def get_model() -> TrainedModel | None:
    return _model
