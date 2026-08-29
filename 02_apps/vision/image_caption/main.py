"""
Image captioning -- write a sentence describing a picture.

What it shows:
    * an encoder-decoder model driven piece by piece (processor -> model -> tokenizer)
    * @st.cache_resource holding all three pieces as one bundle

Model: ydshieh/vit-gpt2-coco-en and friends -- picked in the sidebar.
Reference: https://huggingface.co/docs/transformers/main/tasks/image_captioning

    streamlit run 02_apps/vision/image_caption/main.py
"""

import streamlit as st
from transformers import AutoModelForImageTextToText, AutoImageProcessor, AutoTokenizer
from PIL import Image

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


@st.cache_resource(show_spinner="Loading the model...")
def load_bundle(model_name):
    """Load once and reuse. Keyed on model_name, so switching models reloads.

    transformers 5.x removed the "image-to-text" pipeline task, and the
    replacement "image-text-to-text" pipeline requires a bundled AutoProcessor,
    which older captioning checkpoints like ydshieh/vit-gpt2-coco-en don't ship.
    Load the pieces directly instead, which works either way.
    """
    return {
        "model": AutoModelForImageTextToText.from_pretrained(model_name),
        "image_processor": AutoImageProcessor.from_pretrained(model_name),
        "tokenizer": AutoTokenizer.from_pretrained(model_name),
    }


def main():
    st.header("Image Caption")
    st.divider()
    st.subheader("Step 1: File uploader")
    model_name = utils.sidebar()

    # Defaults to browsing S3; "Upload from my computer" is the fallback.
    my_upload = s3_utils.file_input("image", folder=S3_FOLDER, types=["png", "jpg", "jpeg"])

    if my_upload is not None:
        image = Image.open(my_upload).convert("RGB")
        st.image(image, caption="Uploaded Image", width="stretch")

        st.divider()
        st.subheader("Step 2: Choose a model from left side bar")

        if not model_name:
            st.stop()

        st.write(f'The model you are using is {model_name}')

        st.divider()
        st.subheader("Step 3: Get the caption of the image")

        bundle = load_bundle(model_name)
        pixel_values = bundle["image_processor"](images=image, return_tensors="pt").pixel_values
        output_ids = bundle["model"].generate(pixel_values, max_new_tokens=50)
        caption = bundle["tokenizer"].decode(output_ids[0], skip_special_tokens=True)
        st.write(caption)


if __name__ == "__main__":
    main()
