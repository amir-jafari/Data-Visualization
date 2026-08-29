"""Sidebar, models and plots for the clustering app."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils

# All data for this app lives in S3, never on disk:
#   s3://dats-dl/ajafari@gwu.edu/streamlit/data/data_mining/classification/
S3_FOLDER = "data/data_mining/classification"


def has_umap():
    """UMAP is optional -- offer it only if the install actually works.

    `umap-learn` provides the `umap` module, but an unrelated PyPI package is
    also called `umap` and shadows it. Rather than guess, try the import.
    """
    try:
        import umap
        return hasattr(umap, "UMAP")
    except Exception:
        return False


@st.cache_data(show_spinner=False)
def suggest_eps(X, k=5):
    """A sensible starting eps for DBSCAN: the median distance to the k-th neighbour.

    There is no universal default. In 2 dimensions 0.5 is reasonable; in 30
    standardised dimensions every point is further than that from everything
    else, so DBSCAN labels the entire dataset as noise and you see nothing.
    Reading the scale off the data avoids that dead end.
    """
    neighbours = NearestNeighbors(n_neighbors=k).fit(X)
    distances, _ = neighbours.kneighbors(X)
    return float(np.median(distances[:, -1]))


def sidebar():
    """Pick the algorithm and the 2D projection. Returns (name, params, projection).

    DBSCAN's parameters are *not* set here -- see dbscan_params(). Its `eps` is a
    distance, so it only means anything once we know which space we are
    clustering in, and that depends on a choice made further down the page.
    """
    with st.sidebar:
        st.subheader("Clustering")
        name = st.radio("Algorithm", ["KMeans", "DBSCAN", "Agglomerative"])

        params = {}
        if name == "KMeans":
            params["n_clusters"] = st.slider("Number of clusters (k)", 2, 12, 3)
        elif name == "Agglomerative":
            params["n_clusters"] = st.slider("Number of clusters", 2, 12, 3)

        st.divider()
        st.subheader("Projection")
        choices = ["PCA", "t-SNE"] + (["UMAP"] if has_umap() else [])
        projection = st.radio("Show the clusters in 2D using", choices,
                              help="Squashes the features down to two so the result "
                                   "can be drawn. You can also cluster on it directly.")

    return name, params, projection


def dbscan_params(X):
    """DBSCAN's two knobs, with `eps` scaled to the data being clustered.

    Called after the page knows whether we are clustering in the full feature
    space or in the 2D projection -- those have very different scales, and an
    eps from one is meaningless in the other.
    """
    with st.sidebar:
        st.subheader("DBSCAN")
        default = suggest_eps(X)
        eps = st.slider("eps (neighbourhood radius)",
                        round(default / 4, 2), round(default * 4, 2),
                        round(default, 2), round(default / 20, 3),
                        help="Two points are neighbours if they are closer than this. "
                             "The range is read off your data.")
        st.caption(f"Suggested eps here: **{default:.2f}**")
        min_samples = st.slider("min_samples", 2, 20, 5)

    return {"eps": eps, "min_samples": min_samples}


def build_model(name, params):
    """The one line that differs between the three algorithms."""
    if name == "KMeans":
        return KMeans(n_init=10, random_state=42, **params)
    if name == "DBSCAN":
        return DBSCAN(**params)
    return AgglomerativeClustering(**params)


@st.cache_data(show_spinner="Projecting to 2D...")
def project(X, method, seed=42):
    """Squash many features down to 2 columns, purely so we can plot them."""
    if method == "PCA":
        return PCA(n_components=2, random_state=seed).fit_transform(X)
    if method == "t-SNE":
        # perplexity must stay below the sample count or sklearn refuses.
        perplexity = min(30, max(5, len(X) // 4))
        return TSNE(n_components=2, random_state=seed,
                    perplexity=perplexity, init="pca").fit_transform(X)
    import umap
    return umap.UMAP(n_components=2, random_state=seed).fit_transform(X)


def scatter(coords, labels, method):
    """Draw the 2D projection, one colour per cluster."""
    frame = pd.DataFrame(coords, columns=["x", "y"])
    frame["cluster"] = [str(label) for label in labels]

    # constrained_layout, not tight_layout: the legend sits outside the axes and
    # tight_layout cannot make room for it (it warns and gives up).
    fig, ax = plt.subplots(layout="constrained")
    sns.scatterplot(data=frame, x="x", y="y", hue="cluster",
                    palette="tab10", s=40, ax=ax)
    ax.set(title=f"Clusters, drawn with {method}", xlabel=f"{method} 1", ylabel=f"{method} 2")
    ax.legend(title="cluster", bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig)


def elbow_plot(X, k_max=10):
    """Inertia against k -- the 'elbow' is a common way to choose k."""
    ks = range(2, k_max + 1)
    inertias = [KMeans(n_clusters=k, n_init=10, random_state=42).fit(X).inertia_ for k in ks]

    fig, ax = plt.subplots()
    ax.plot(list(ks), inertias, marker="o")
    ax.set(xlabel="k", ylabel="inertia (within-cluster sum of squares)",
           title="Elbow plot -- look for where the curve stops dropping sharply")
    fig.tight_layout()
    st.pyplot(fig)


def quality(X, labels):
    """Silhouette score, guarded for the cases where it is undefined."""
    unique = set(labels)
    n_clusters = len(unique - {-1})     # -1 is DBSCAN's "noise" label

    if n_clusters < 2:
        st.warning("Only one cluster was found -- silhouette score needs at least two. "
                   "Try different parameters.")
        return

    # DBSCAN's noise points are not a cluster, so leave them out of the score.
    mask = [label != -1 for label in labels]
    score = silhouette_score(X[mask], [l for l in labels if l != -1])

    col1, col2 = st.columns(2)
    col1.metric("Clusters found", n_clusters)
    col2.metric("Silhouette score", f"{score:.3f}",
                help="-1 to 1. Above ~0.5 is a clear structure; near 0 means "
                     "the clusters overlap.")


def upload_file(label):
    """Browse S3 by default; uploading your own CSV is the fallback."""
    file = s3_utils.file_input(label, folder=S3_FOLDER, types=["csv"])
    if file is None:
        return None

    data = pd.read_csv(file)
    st.write(data.head())
    return data
