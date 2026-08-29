"""
The other half of the project -- a Streamlit front end for the Data API.

This is the point of the whole exercise. The API knows about data and models
and nothing about screens; this page knows about screens and nothing about
data. They talk over HTTP, and either one can be rewritten without touching
the other.

Run BOTH, in two terminals:

    python fastapi/project/serve.py                     # terminal 1, port 8000
    streamlit run fastapi/project/client.py             # terminal 2, port 8501

Notice what this file does NOT contain: no pandas loading, no S3, no model.
It asks the API. That separation is why the API can be deployed once and used
by this page, a notebook, a phone app, or a colleague's script.
"""

import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
TIMEOUT = 30

st.set_page_config(page_title="Data API client", page_icon="🔌", layout="wide")


# --------------------------------------------------------------------------- #
# talking to the API
# --------------------------------------------------------------------------- #
def api_get(path, **params):
    """One place that knows how to call the API, and how it can fail."""
    try:
        response = requests.get(f"{API_URL}{path}", params=params, timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        st.error(
            f"### The API is not running\n\n"
            f"This page reads everything from `{API_URL}`, and nothing is "
            f"listening there.\n\n"
            f"Start it in another terminal:\n\n"
            f"```bash\npython fastapi/project/serve.py\n```"
        )
        st.stop()
    except requests.exceptions.Timeout:
        st.error(f"The API did not answer within {TIMEOUT} seconds.")
        st.stop()

    if response.status_code >= 400:
        detail = response.json().get("detail", response.text)
        st.error(f"API returned {response.status_code}: {detail}")
        st.stop()
    return response.json()


def api_post(path, payload, api_key):
    try:
        response = requests.post(f"{API_URL}{path}", json=payload,
                                 headers={"X-API-Key": api_key}, timeout=TIMEOUT)
    except requests.exceptions.RequestException as exc:
        st.error(f"Could not reach the API: {exc}")
        return None

    if response.status_code == 401:
        st.error("The API rejected that key. The default is `student-key`.")
        return None
    if response.status_code >= 400:
        st.error(f"API returned {response.status_code}: {response.text}")
        return None
    return response.json()


# --------------------------------------------------------------------------- #
# sidebar
# --------------------------------------------------------------------------- #
health = api_get("/health")

with st.sidebar:
    st.subheader("API")
    st.caption(API_URL)
    col1, col2 = st.columns(2)
    col1.metric("Datasets", health["datasets"])
    col2.metric("Version", health["version"])
    st.write("Model ready:", "yes" if health["model_ready"] else "no")
    st.write("S3 reachable:", "yes" if health["s3"] else "no (using built-in data)")
    st.divider()
    api_key = st.text_input("API key", value="student-key", type="password",
                            help="Needed only for predictions")
    st.caption(f"[Interactive API docs]({API_URL}/docs)")

st.title("Course Data API — client")
st.write("Everything on this page came from the API over HTTP. "
         "There is no pandas, no S3 and no model in this file.")

catalog = api_get("/datasets")
names = [d["name"] for d in catalog]

tab_browse, tab_summary, tab_predict = st.tabs(["Browse", "Summary", "Predict"])

# --------------------------------------------------------------------------- #
with tab_browse:
    st.subheader("Browse a dataset")

    chosen = st.selectbox("Dataset", names, key="browse_dataset")
    info = next(d for d in catalog if d["name"] == chosen)
    st.caption(f"{info['rows']:,} rows · {len(info['columns'])} columns · "
               f"source: {info['source']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        limit = st.slider("Rows per page", 5, 200, 25)
    with col2:
        column = st.selectbox("Filter column", ["(none)"] + info["columns"])
    with col3:
        equals = st.text_input("equals", disabled=(column == "(none)"))

    page_number = st.number_input("Page", min_value=1, value=1, step=1)
    offset = (page_number - 1) * limit

    params = {"limit": limit, "offset": offset}
    if column != "(none)" and equals:
        params |= {"column": column, "equals": equals}

    page = api_get(f"/datasets/{chosen}", **params)

    st.write(f"Showing rows {page['offset'] + 1}–{page['offset'] + page['returned']} "
             f"of {page['total']:,}")
    st.dataframe(pd.DataFrame(page["rows"]))

    st.caption(f"GET {API_URL}/datasets/{chosen}?"
               + "&".join(f"{k}={v}" for k, v in params.items()))
    st.link_button("Download the whole thing as CSV",
                   f"{API_URL}/datasets/{chosen}/export.csv")

# --------------------------------------------------------------------------- #
with tab_summary:
    st.subheader("Column summary")

    chosen = st.selectbox("Dataset", names, key="summary_dataset")
    summary = api_get(f"/datasets/{chosen}/summary")

    frame = pd.DataFrame(summary["columns"])
    st.write(f"{summary['rows']:,} rows")
    st.dataframe(frame)

    numeric = frame.dropna(subset=["mean"])
    if not numeric.empty:
        st.write("**Mean by column**")
        st.bar_chart(numeric.set_index("column")["mean"])

    missing = frame[frame["missing"] > 0]
    if not missing.empty:
        st.write("**Missing values**")
        st.bar_chart(missing.set_index("column")["missing"])
    else:
        st.caption("No missing values in this dataset.")

# --------------------------------------------------------------------------- #
with tab_predict:
    st.subheader("Ask the model")

    if not health["model_ready"]:
        st.warning("The API reports that no model is loaded, so this tab cannot work.")
        st.stop()

    info = api_get("/model/info")
    col1, col2, col3 = st.columns(3)
    col1.metric("Model", info["model_name"])
    col2.metric("Trained on", info["trained_on"])
    col3.metric("Test accuracy", f"{info['test_accuracy'] * 100:.1f} %")

    st.write(f"It expects {info['n_features']} features. "
             f"Fill in the first few — the rest default to 0.")

    shown = info["features"][:6]
    values = {}
    columns = st.columns(3)
    for i, feature in enumerate(shown):
        with columns[i % 3]:
            values[feature] = st.number_input(feature, value=0.0, format="%.4f")

    if st.button("Predict", type="primary"):
        result = api_post("/model/predict", {"rows": [values]}, api_key)
        if result:
            prediction = result["predictions"][0]
            st.success(f"**{prediction['prediction']}** "
                       f"({prediction['confidence'] * 100:.1f}% confident)")
            st.caption("POST /model/predict — the only route that needs the key")
