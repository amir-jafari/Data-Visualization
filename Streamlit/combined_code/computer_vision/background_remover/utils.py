from io import BytesIO

import streamlit as st
from PIL import Image
from rembg import remove


# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


# Package the transform into a function
def fix_image(upload):
    # Create the columns
    col1, col2 = st.columns(2)

    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    fixed = remove(image)
    col2.write("Fixed Image :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button(
        "Download fixed image", convert_image(fixed), "fixed.png", "image/png"
    )
