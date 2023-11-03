# Reference: https://blog.streamlit.io/build-an-image-background-remover-in-streamlit/

import streamlit as st
import utils


def main():
    st.set_page_config(layout="wide", page_title="Image Background Remover")

    st.write("## Remove background from your image")
    st.write(
        ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](<https://github.com/tyler-simons/BackgroundRemoval>) on GitHub. Special thanks to the [rembg library](<https://github.com/danielgatis/rembg>) :grin:"
    )
    st.sidebar.write("## Upload and download :gear:")

    # Create the file uploader
    my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    # Fix the image!
    if my_upload is not None:
        utils.fix_image(upload=my_upload)


if __name__ == "__main__":
    main()
