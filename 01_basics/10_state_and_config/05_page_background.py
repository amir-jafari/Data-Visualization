import streamlit as st
import base64

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils

st.subheader("***Background***")
st.write('Setup the webpage background. The image comes from S3, not from disk.')


with st.echo():
    @st.cache_data
    def set_png_as_page_bg(image_bytes):
        bin_str = base64.b64encode(image_bytes).decode()
        page_bg_img = '''
        <style>
        .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: scroll; # doesn't work
        }
        </style>
        ''' % bin_str

        st.markdown(page_bg_img, unsafe_allow_html=True)
        return


    # s3://dats-dl/ajafari@gwu.edu/streamlit/static/background.webp
    # read_bytes() stops the app with a "keys need updating" message if S3 refuses us.
    set_png_as_page_bg(s3_utils.read_bytes('static/background.webp'))

st.caption(f"Source: {s3_utils.uri('static/background.webp')}")
