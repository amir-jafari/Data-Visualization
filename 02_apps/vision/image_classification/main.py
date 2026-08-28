# https://huggingface.co/google/vit-base-patch16-224

# from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import streamlit as st
from transformers import pipeline

import utils

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils

# All data for this app lives in S3, never on disk:
#   s3://dats-dl/ajafari@gwu.edu/streamlit/data/computer_vision/
S3_FOLDER = "data/computer_vision"


def main():
    st.header("Image Classification")
    st.divider()
    st.subheader("Step 1: File uploader")

    model_name = utils.sidebar()

    # Defaults to browsing S3; "Upload from my computer" is the fallback.
    my_upload = s3_utils.file_input("image", folder=S3_FOLDER, types=["png", "jpg", "jpeg"])

    if my_upload is None:
        st.stop()

    image = Image.open(my_upload)
    st.image(image, caption="Uploaded Image", width="stretch")

    st.divider()
    st.subheader("Step 2: Choose a model from left side bar")

    if not model_name:
        st.stop()

    st.write(f'The model you are using is {model_name}')

    st.divider()
    st.subheader("Step 3: Predict the image")

    if 'pipe' not in st.session_state:
        st.session_state['pipe'] = pipeline("image-classification", model=model_name)

    # classification_pipeline = pipeline("image-classification", model=model_name)
    result = st.session_state['pipe'](image)
    print(result)

    st.write(f"Predicted class: {result[0]['label']}")


if __name__ == "__main__":
    main()
