# https://albumentations.ai/docs/

import streamlit as st
import numpy as np
import random
import cv2
import albumentations as A

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
    st.header("Data augmentation")
    st.divider()
    st.subheader("Step 1: File uploader")
    selected = utils.sidebar()

    # Defaults to browsing S3; "Upload from my computer" is the fallback.
    my_upload = s3_utils.file_input("image", folder=S3_FOLDER, types=["png", "jpg", "jpeg"])

    if my_upload is not None:
        # To read file as bytes:
        file_bytes = np.asarray(bytearray(my_upload.read()), dtype=np.uint8)

        # Use OpenCV to read the file
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        st.image(image, caption="Uploaded Image", width="stretch")

        st.divider()
        st.subheader("Step 2: Some data augmentation demos")

        col1, col2, col3 = st.columns(3)

        with col1:
            utils.do_image_augment(image, 'A.HorizontalFlip(p=1)')
            utils.do_image_augment(image, 'A.Blur(blur_limit=101, p=1)')
            utils.do_image_augment(image, 'A.ToGray(p=1)')

        with col2:
            utils.do_image_augment(image, 'A.VerticalFlip(p=1)')
            utils.do_image_augment(image, 'A.OpticalDistortion(p=1)')
            utils.do_image_augment(image, 'A.RandomBrightnessContrast(brightness_limit=0.8, contrast_limit=0.8, p=1)')

        with col3:
            utils.do_image_augment(image, 'A.Affine(translate_percent=(-0.0625, 0.0625), scale=(0.9, 1.1), rotate=(-45, 45), p=1)')
            utils.do_image_augment(image, 'A.GridDistortion(p=1)')
            utils.do_image_augment(image, 'A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=1)')

        st.divider()
        st.subheader("Step 3: Create your own augmented image from left side bar")

        if st.button('Finish choosing', type="primary"):
            if not selected:
                st.error("No data augmentation methods selected")
                st.stop()

            aug_str = ', '.join(item[1] for item in selected)
            st.write(f'You will use the following methods: ***{aug_str}***')

            aug_lst = [item[0] for item in selected]
            transform = A.Compose(aug_lst)
            # random.seed(42)
            augmented_image = transform(image=image)['image']
            st.image(augmented_image, caption="augmented Image", width="content")


if __name__ == "__main__":
    main()
