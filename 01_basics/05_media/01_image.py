import streamlit as st

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils

# %%--------------------------------------------------------------------------------------------------------------------
st.header("Media elements")
st.write("It's easy to embed images, videos, and audio files directly into your Streamlit apps.")
st.write("The media below is not on disk -- it is pulled from S3 every time this page runs.")


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Image***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    # s3://dats-dl/ajafari@gwu.edu/streamlit/static/flower.png
    # read_image() stops the app with a "keys need updating" message if S3 refuses us.
    image = s3_utils.read_image('static/flower.png')

    st.image(image, caption='A beautiful flower')

st.caption(f"Source: {s3_utils.uri('static/flower.png')}")
