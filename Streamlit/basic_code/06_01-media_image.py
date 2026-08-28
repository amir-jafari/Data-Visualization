import streamlit as st

# --- make Streamlit/s3_utils.py importable from any sub-folder ----------------
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents
                            if (p / "s3_utils.py").is_file())))
import s3_utils

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
