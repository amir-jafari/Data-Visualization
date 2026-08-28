import torch
import streamlit as st
from PIL import Image

import utils2

# --- make Streamlit/s3_utils.py importable from any sub-folder ----------------
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents
                            if (p / "s3_utils.py").is_file())))
import s3_utils

# All data for this app lives in S3, never on disk:
#   s3://dats-dl/ajafari@gwu.edu/streamlit/data/computer_vision/object_detection/
S3_FOLDER = "data/computer_vision/object_detection"



def main():
    st.header("Object detection")
    st.divider()
    st.subheader("Step 1: File uploader")
    model_name = utils2.sidebar()

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
        st.subheader("Step 3: Start object detection")

        if model_name not in st.session_state:
            # Load the YOLOv5 model
            st.session_state[model_name] = torch.hub.load(model_name, 'yolov5s', pretrained=True)

        results = st.session_state[model_name](image)

        results_img = results.render()[0]  # This is a PIL Image
        results_img_pil = Image.fromarray(results_img)

        # Use Streamlit to write the image to the webpage
        st.image(results_img_pil, caption='Detected Objects', use_column_width=True)


if __name__ == "__main__":
    main()
