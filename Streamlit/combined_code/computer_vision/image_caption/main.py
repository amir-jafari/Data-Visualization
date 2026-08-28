# https://medium.com/@sirikrrishna99/automatic-image-captioning-using-streamlit-and-hugging-face-transformers-d3563edb5457
# https://huggingface.co/docs/transformers/main/tasks/image_captioning

import streamlit as st
from transformers import AutoModelForImageTextToText, AutoImageProcessor, AutoTokenizer
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
        image = Image.open(my_upload).convert("RGB")
        st.image(image, caption="Uploaded Image", width="stretch")

        st.divider()
        st.subheader("Step 2: Choose a model from left side bar")

        if not model_name:
            st.stop()

        st.write(f'The model you are using is {model_name}')

        st.divider()
        st.subheader("Step 3: Get the caption of the image")

        if model_name not in st.session_state:
            # transformers 5.x removed the "image-to-text" pipeline task, and the
            # replacement "image-text-to-text" pipeline requires a bundled
            # AutoProcessor, which older captioning checkpoints like
            # ydshieh/vit-gpt2-coco-en don't ship. Load the pieces directly instead,
            # which works whether or not the repo has a combined processor.
            st.session_state[model_name] = {
                "model": AutoModelForImageTextToText.from_pretrained(model_name),
                "image_processor": AutoImageProcessor.from_pretrained(model_name),
                "tokenizer": AutoTokenizer.from_pretrained(model_name),
            }

        bundle = st.session_state[model_name]
        pixel_values = bundle["image_processor"](images=image, return_tensors="pt").pixel_values
        output_ids = bundle["model"].generate(pixel_values, max_new_tokens=50)
        caption = bundle["tokenizer"].decode(output_ids[0], skip_special_tokens=True)
        st.write(caption)


if __name__ == "__main__":
    main()
