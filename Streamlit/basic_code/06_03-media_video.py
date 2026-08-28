import streamlit as st

# --- make Streamlit/s3_utils.py importable from any sub-folder ----------------
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents
                            if (p / "s3_utils.py").is_file())))
import s3_utils

st.subheader("***Video***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    # s3://dats-dl/ajafari@gwu.edu/streamlit/static/myvideo.mp4
    # read_bytes() stops the app with a "keys need updating" message if S3 refuses us.
    video_bytes = s3_utils.read_bytes('static/myvideo.mp4')

    st.video(video_bytes)

st.caption(f"Source: {s3_utils.uri('static/myvideo.mp4')}")
