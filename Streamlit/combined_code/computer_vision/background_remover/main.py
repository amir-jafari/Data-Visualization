# Reference: https://blog.streamlit.io/build-an-image-background-remover-in-streamlit/

import streamlit as st
import utils

# --- make Streamlit/s3_utils.py importable from any sub-folder ----------------
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents
                            if (p / "s3_utils.py").is_file())))
import s3_utils

# All data for this app lives in S3, never on disk:
#   s3://dats-dl/ajafari@gwu.edu/streamlit/data/computer_vision/background_remover/
S3_FOLDER = "data/computer_vision/background_remover"



def main():
    st.set_page_config(layout="wide", page_title="Image Background Remover")

    st.write("## Remove background from your image")
    st.write(
        ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](<https://github.com/tyler-simons/BackgroundRemoval>) on GitHub. Special thanks to the [rembg library](<https://github.com/danielgatis/rembg>) :grin:"
    )
    st.sidebar.write("## Upload and download :gear:")

    # Create the file uploader
    # Defaults to browsing S3; "Upload from my computer" is the fallback.
    my_upload = s3_utils.file_input("image", folder=S3_FOLDER,
                                    types=["png", "jpg", "jpeg"], container=st.sidebar)

    # Fix the image!
    if my_upload is not None:
        utils.fix_image(upload=my_upload)


if __name__ == "__main__":
    main()
