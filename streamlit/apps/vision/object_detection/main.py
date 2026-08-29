"""
Object detection -- draw boxes around everything YOLOv5 recognises in a picture.

What it shows:
    * torch.hub loading a model straight from a GitHub repo
    * @st.cache_resource, so the weights are fetched once per model

Model: ultralytics/yolov5 (yolov5s) -- picked in the sidebar.

    streamlit run streamlit/apps/vision/object_detection/main.py
"""

import torch
import streamlit as st
from PIL import Image

import utils

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils

# All data for this app lives in S3, never on disk:
#   s3://dats-dl/ajafari@gwu.edu/streamlit/data/computer_vision/object_detection/
S3_FOLDER = "data/computer_vision/object_detection"


@st.cache_resource(show_spinner="Loading the model...")
def load_model(model_name):
    """Load once and reuse. Keyed on model_name, so switching models reloads."""
    # torch.hub clones/caches the yolov5 repo and its own models/common.py does
    # `from utils import TryExcept`, expecting *its* utils/ package. Our
    # `import utils` above already cached this app's sibling utils.py under that
    # same name, so without dropping it here yolov5 would silently get our
    # module instead of its own and fail to import.
    sys.modules.pop("utils", None)
    return torch.hub.load(model_name, 'yolov5s', pretrained=True)


def main():
    st.header("Object detection")
    st.divider()
    st.subheader("Step 1: File uploader")
    model_name = utils.sidebar()

    # Defaults to browsing S3; "Upload from my computer" is the fallback.
    my_upload = s3_utils.file_input("image", folder=S3_FOLDER, types=["png", "jpg", "jpeg"])

    if my_upload is not None:
        image = Image.open(my_upload)
        st.image(image, caption="Uploaded Image", width="stretch")

        st.divider()
        st.subheader("Step 2: Choose a model from left side bar")

        if not model_name:
            st.stop()

        st.write(f'The model you are using is {model_name}')

        st.divider()
        st.subheader("Step 3: Start object detection")

        model = load_model(model_name)
        results = model(image)

        results_img = Image.fromarray(results.render()[0])
        st.image(results_img, caption='Detected Objects', width="stretch")


if __name__ == "__main__":
    main()
