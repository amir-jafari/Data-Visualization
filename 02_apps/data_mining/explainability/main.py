"""
Explainability -- ask a trained model *why* it predicted what it did.

classification/ tells you a model is 94% accurate. This one asks the next
question, which is the one that actually gets a model used: what is it
relying on, and would you trust this particular prediction?

What it shows:
    * global explanation -- which features drive the model overall, from SHAP,
      next to the model's own feature_importances_ (they often disagree, and
      the disagreement is the lesson)
    * local explanation -- pick one row and see exactly which features pushed
      that single prediction up or down (SHAP waterfall)
    * the same single row explained by LIME, a completely different method, so
      you can see where two explanations agree and where they do not

Models: tree-based, so SHAP has an exact fast path. SHAP itself is
model-agnostic -- the tree models just make it quick enough for a live demo.

Data: browsed from S3 (data/data_mining/classification), or upload your own.

    streamlit run 02_apps/data_mining/explainability/main.py
"""

import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

import utils


def main():
    st.header("Model Explainability")
    st.divider()
    st.subheader("Step 1: Load the data")

    data = utils.upload_file("CSV data file")
    if data is None:
        st.stop()

    # A trailing comma on every line of a CSV gains a phantom, entirely-empty
    # column. Left in, it would make every row look incomplete.
    empty = [c for c in data.columns if data[c].isnull().all()]
    if empty:
        data = data.drop(columns=empty)
        st.info(f"Ignored {len(empty)} completely empty column(s): {', '.join(map(str, empty))}.")

    st.divider()
    st.subheader("Step 2: Choose what to predict")

    target = st.selectbox("Target column", data.columns,
                          help="The thing the model should learn to predict.")

    features = st.multiselect(
        "Features",
        [c for c in data.select_dtypes("number").columns if c != target],
        default=[c for c in data.select_dtypes("number").columns if c != target],
        help="Numeric columns only. Drop ID-like columns -- a model can memorise "
             "them, and then the explanation is meaningless.")

    if len(features) < 2:
        st.warning("Pick at least two features.")
        st.stop()

    frame = data[features + [target]].dropna()
    if frame.empty:
        st.error("No rows left after dropping missing values. Try other columns.")
        st.stop()

    X = frame[features]
    y_raw = frame[target]

    # SHAP and the classifiers want numeric classes; keep the original names for labels.
    encoder = LabelEncoder()
    y = encoder.fit_transform(y_raw)

    if len(encoder.classes_) < 2:
        st.error(f"`{target}` only has one distinct value -- there is nothing to predict.")
        st.stop()
    if len(encoder.classes_) > 10:
        st.error(f"`{target}` has {len(encoder.classes_)} distinct values, which looks "
                 f"like an ID or a continuous number rather than a class. Pick another.")
        st.stop()

    st.caption(f"{len(X)} rows, {len(features)} features, "
               f"{len(encoder.classes_)} classes: {', '.join(map(str, encoder.classes_))}")

    st.divider()
    st.subheader("Step 3: Train")

    name, params = utils.sidebar()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)

    model = utils.train(name, tuple(sorted(params.items())), X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test)) * 100

    col1, col2 = st.columns(2)
    col1.metric("Model", name)
    col2.metric("Test accuracy", f"{accuracy:.1f} %")
    st.caption("Accuracy tells you *whether* to trust the model. The rest of this "
               "page tells you *why* it decided what it did.")

    st.divider()
    st.subheader("Step 4: What does the model rely on overall?")

    explanation = utils.shap_values(
        model, X_test, cache_key=f"{name}|{sorted(params.items())}|{tuple(features)}|{len(X_test)}")

    utils.global_plots(explanation, features)

    with st.expander("Compare with the model's own feature_importances_"):
        st.write("Tree models expose their own importance score. It measures how much "
                 "each feature reduced impurity while *training*, whereas SHAP measures "
                 "how much each feature moved the *predictions*. They frequently "
                 "disagree -- built-in importance is biased towards high-cardinality "
                 "features, and it cannot tell you which direction a feature pushed.")
        table = utils.importance_table(model, features)
        if table is None:
            st.caption("This model does not expose feature_importances_.")
        else:
            st.dataframe(table)

    st.divider()
    st.subheader("Step 5: Why this particular prediction?")

    index = st.slider("Which test row?", 0, len(X_test) - 1, 0)

    actual = encoder.classes_[y_test[index]]
    predicted = encoder.classes_[model.predict(X_test.iloc[[index]])[0]]

    col1, col2 = st.columns(2)
    col1.metric("Actual", str(actual))
    col2.metric("Predicted", str(predicted),
                delta="correct" if actual == predicted else "wrong",
                delta_color="normal" if actual == predicted else "inverse")

    st.write("***SHAP*** -- every feature's contribution, starting from the average "
             "prediction and ending at this row's.")
    utils.local_plot(explanation, index)

    if utils.has_lime():
        st.write("***LIME*** -- the same row, explained by fitting a simple model to "
                 "small perturbations around it. A second opinion, arrived at a "
                 "completely different way.")
        utils.lime_plot(model, X_train, X_test.iloc[index], encoder.classes_)
    else:
        st.info("LIME is not installed, so only the SHAP explanation is shown. "
                "`pip install lime` to see the two side by side.")


if __name__ == "__main__":
    main()
