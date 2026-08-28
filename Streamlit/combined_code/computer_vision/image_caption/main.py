# https://medium.com/@sirikrrishna99/automatic-image-captioning-using-streamlit-and-hugging-face-transformers-d3563edb5457
# https://huggingface.co/docs/transformers/main/tasks/image_captioning

import streamlit as st
from transformers import pipeline
from PIL import Image

import utils

# --- make Streamlit/s3_utils.py importable from any sub-folder ----------------
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents
                            if (p / "s3_utils.py").is_file())))
import s3_utils

# All data for this app lives in S3, never on disk:
#   s3://dats-dl/ajafari@gwu.edu/streamlit/data/computer_vision/
S3_FOLDER = "data/computer_vision"



def main():
    st.header("Image Caption")
    st.divider()
    st.subheader("Step 1: File uploader")
    model_name = utils.sidebar()

    # Defaults to browsing S3; "Upload from my computer" is the fallback.
    my_upload = s3_utils.file_input("image", folder=S3_FOLDER, types=["png", "jpg", "jpeg"])

    if my_upload is not None:
        image = Image.open(my_upload)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.divider()
        st.subheader("Step 2: Choose a model from left side bar")

        if not model_name:
            st.stop()

        st.write(f'The model you are using is {model_name}')

        st.divider()
        st.subheader("Step 3: Get the caption of the image")

        if model_name not in st.session_state:
            st.session_state[model_name] = pipeline('image-to-text', model=model_name)

        captions = st.session_state[model_name](image)
        st.write(captions[0]['generated_text'])


if __name__ == "__main__":
    main()
