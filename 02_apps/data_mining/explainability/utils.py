"""Sidebar, model training and explanation plots for the explainability app."""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import shap
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils

# All data for this app lives in S3, never on disk:
#   s3://dats-dl/ajafari@gwu.edu/streamlit/data/data_mining/classification/
S3_FOLDER = "data/data_mining/classification"

MODELS = {
    "Random Forest": RandomForestClassifier,
    "Gradient Boosting": GradientBoostingClassifier,
    "Decision Tree": DecisionTreeClassifier,
}


def has_lime():
    """LIME is optional -- offer it only if it is installed."""
    try:
        import lime.lime_tabular  # noqa: F401
        return True
    except Exception:
        return False


def sidebar():
    """Pick the model and its parameters. Returns (name, params dict)."""
    with st.sidebar:
        st.subheader("Model")
        name = st.radio("Classifier", list(MODELS))

        params = {"random_state": 42}
        if name == "Decision Tree":
            params["max_depth"] = st.slider("max_depth", 1, 15, 4)
        else:
            params["max_depth"] = st.slider("max_depth", 1, 15, 5)
            if name == "Random Forest":
                params["n_estimators"] = st.slider("n_estimators", 10, 300, 100, 10)
            else:
                params["n_estimators"] = st.slider("n_estimators", 10, 300, 100, 10)
                params["learning_rate"] = st.slider("learning_rate", 0.01, 1.0, 0.1, 0.01)

    return name, params


@st.cache_resource(show_spinner="Training...")
def train(name, params_items, X, y):
    """Fit the chosen model. Cached, so changing only the row you inspect
    below does not retrain everything.

    params arrives as a tuple of items because a dict cannot be a cache key.
    """
    model = MODELS[name](**dict(params_items))
    model.fit(X, y)
    return model


@st.cache_data(show_spinner="Computing SHAP values...")
def shap_values(_model, X, cache_key):
    """SHAP values for every row of X.

    `_model` is underscore-prefixed so Streamlit does not try to hash it;
    `cache_key` is what actually identifies this result instead.

    Binary classifiers come back in one of two shapes depending on the model:
    (rows, features) or (rows, features, classes). Normalise to the first, so
    everything downstream sees "the effect on the positive class".

    TreeExplainer with no background dataset uses the exact tree-path method:
    fast, and it avoids the additivity mismatch that gradient boosting hits
    when SHAP has to approximate against a background sample instead.
    """
    explanation = shap.TreeExplainer(_model)(X)
    if explanation.values.ndim == 3:
        explanation = explanation[:, :, 1]
    return explanation


def global_plots(explanation, feature_names):
    """What the model relies on overall, across every row."""
    tab1, tab2 = st.tabs(["Which features matter most", "How they push predictions"])

    with tab1:
        st.write("Mean absolute SHAP value per feature -- the model's overall reliance.")
        fig = plt.figure()
        shap.plots.bar(explanation, show=False)
        st.pyplot(fig, clear_figure=True)

    with tab2:
        st.write("One dot per row. Position = how much that feature pushed *that* "
                 "prediction; colour = whether the feature was high or low.")
        fig = plt.figure()
        shap.plots.beeswarm(explanation, show=False)
        st.pyplot(fig, clear_figure=True)


def local_plot(explanation, index):
    """Why the model predicted what it did for one single row."""
    fig = plt.figure()
    shap.plots.waterfall(explanation[index], show=False)
    st.pyplot(fig, clear_figure=True)


def lime_plot(model, X_train, row, class_names, n_features=10):
    """The same single-row question, answered a completely different way."""
    from lime.lime_tabular import LimeTabularExplainer

    explainer = LimeTabularExplainer(
        X_train.values,
        feature_names=list(X_train.columns),
        class_names=[str(c) for c in class_names],
        mode="classification",
        random_state=42,
    )
    # LIME hands the model plain numpy arrays. sklearn was fitted on a
    # DataFrame and warns about the missing column names, so put them back.
    def predict_proba(array):
        return model.predict_proba(pd.DataFrame(array, columns=X_train.columns))

    explanation = explainer.explain_instance(
        row.values, predict_proba, num_features=n_features)

    fig = explanation.as_pyplot_figure()
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)


def importance_table(model, feature_names):
    """The model's own built-in importances, for comparison with SHAP."""
    if not hasattr(model, "feature_importances_"):
        return None
    return (pd.DataFrame({"feature": feature_names,
                          "importance": model.feature_importances_})
            .sort_values("importance", ascending=False)
            .reset_index(drop=True))


def upload_file(label):
    """Browse S3 by default; uploading your own CSV is the fallback."""
    file = s3_utils.file_input(label, folder=S3_FOLDER, types=["csv"])
    if file is None:
        return None
    data = pd.read_csv(file)
    st.write(data.head())
    return data
