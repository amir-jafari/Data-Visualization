"""
Clustering -- find groups in data that has no labels.

The unsupervised counterpart to classification/. There, every row came with
the right answer; here nothing does, and the job is to discover the structure.

What it shows:
    * three algorithms that disagree in useful ways: KMeans (round clusters,
      you choose k), DBSCAN (any shape, finds k itself, labels outliers as
      noise) and Agglomerative (merges rows bottom-up)
    * why scaling matters -- distance-based methods are dominated by whichever
      column happens to have the biggest units
    * projecting many features down to 2 with PCA / t-SNE / UMAP, purely so
      the result can be drawn
    * judging a clustering with no ground truth: silhouette score and the
      elbow plot

Data: browsed from S3 (data/data_mining/classification), or upload your own.
Any numeric CSV works -- the label column, if there is one, is just dropped.

    streamlit run 02_apps/data_mining/clustering/main.py
"""

import streamlit as st
from sklearn.preprocessing import StandardScaler

import utils


def main():
    st.header("Clustering")
    st.divider()
    st.subheader("Step 1: Load the data")

    data = utils.upload_file("CSV data file")
    if data is None:
        st.stop()

    st.divider()
    st.subheader("Step 2: Choose the columns to cluster on")

    numeric = data.select_dtypes("number")

    # A CSV with a trailing comma on every line gains a phantom, entirely-empty
    # column (pandas calls it "Unnamed: N"). Left in, the dropna() below would
    # throw away *every* row. Real gotcha, worth seeing.
    empty = [c for c in numeric.columns if numeric[c].isnull().all()]
    if empty:
        numeric = numeric.drop(columns=empty)
        st.info(f"Ignored {len(empty)} completely empty column(s): "
                f"{', '.join(map(str, empty))}. Every row is missing a value there, "
                f"so keeping them would drop the whole dataset.")

    if numeric.shape[1] < 2:
        st.error("This file has fewer than two usable numeric columns, so there is "
                 "nothing to cluster on. Try another dataset.")
        st.stop()

    features = st.multiselect(
        "Features (numeric columns only)",
        list(numeric.columns),
        default=list(numeric.columns),
        help="Clustering has no target column. If this file has a label column, "
             "leave it out here -- then compare it to the clusters at the end.")

    if len(features) < 2:
        st.warning("Pick at least two features.")
        st.stop()

    X = numeric[features].dropna()
    if X.empty:
        st.error("No rows survive once rows with missing values are dropped. "
                 "Deselect whichever column is mostly empty and try again.")
        st.stop()
    st.caption(f"{len(X)} of {len(data)} rows kept after dropping missing values.")

    scale = st.toggle(
        "Standardise the features (recommended)", value=True,
        help="KMeans and DBSCAN measure distance, so a column in the thousands "
             "would drown out a column between 0 and 1. Standardising puts every "
             "column on the same footing.")

    X_used = StandardScaler().fit_transform(X) if scale else X.values

    st.divider()
    st.subheader("Step 3: Cluster")

    name, params, projection = utils.sidebar()
    st.write(f"Algorithm: ***{name}*** -- change it in the sidebar.")

    coords = utils.project(X_used, projection)

    on_projection = st.toggle(
        f"Cluster on the 2D {projection} projection instead of all {X_used.shape[1]} features",
        value=False,
        help="Distance-based clustering gets unreliable in high dimensions -- "
             "everything ends up roughly equally far from everything else. "
             "Reducing first, then clustering, is a standard way around it, and "
             "it is what makes DBSCAN usable here.")

    X_cluster = coords if on_projection else X_used

    # DBSCAN's eps is a distance, so it can only be chosen once we know which
    # space we are in -- hence the extra sidebar section here rather than above.
    if name == "DBSCAN":
        params = utils.dbscan_params(X_cluster)

    model = utils.build_model(name, params)
    labels = model.fit_predict(X_cluster)

    utils.quality(X_cluster, labels)

    if name == "DBSCAN":
        noise = sum(1 for label in labels if label == -1)
        clusters = len(set(labels) - {-1})

        if clusters < 2 and not on_projection and X_used.shape[1] > 5:
            st.warning(
                f"DBSCAN found {clusters} cluster(s) across {X_used.shape[1]} features. "
                f"That is the **curse of dimensionality**: in that many dimensions the "
                f"distances between points all look alike, so no neighbourhood is dense "
                f"enough to seed a cluster. Two things to try -- turn on the projection "
                f"toggle above, or widen `eps` in the sidebar.")
        elif noise:
            st.info(f"DBSCAN labelled {noise} of {len(labels)} rows as **noise** "
                    f"(cluster -1). That is a feature, not a bug -- unlike KMeans it "
                    f"refuses to force every point into a group.")

    st.divider()
    st.subheader("Step 4: See the clusters")

    utils.scatter(coords, labels, projection)

    st.divider()
    st.subheader("Step 5: How many clusters should there be?")

    if name != "KMeans":
        st.write("The elbow plot is a KMeans tool -- KMeans is the algorithm that makes "
                 "you commit to k up front. It is shown here anyway, as a second opinion "
                 "on how many groups this data really has.")
    utils.elbow_plot(X_cluster)

    with st.expander("Compare the clusters against a real column"):
        st.write("Clustering never saw any labels. If your file has one, this shows "
                 "how well the discovered groups line up with it.")
        other = [c for c in data.columns if c not in features]
        if not other:
            st.caption("No spare column in this file to compare against.")
        else:
            truth = st.selectbox("Column to compare against", other)
            comparison = data.loc[X.index, truth].to_frame("actual")
            comparison["cluster"] = labels
            st.write(comparison.groupby(["cluster", "actual"]).size()
                     .unstack(fill_value=0))


if __name__ == "__main__":
    main()
