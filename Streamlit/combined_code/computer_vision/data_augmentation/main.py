# https://albumentations.ai/docs/

import streamlit as st
import numpy as np
import random
import cv2
import albumentations as A

import utils


def main():
    st.header("Data augmentation")
    st.divider()
    st.subheader("Step 1: File uploader")
    selected = utils.sidebar()

    my_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if my_upload is not None:
        # To read file as bytes:
        file_bytes = np.asarray(bytearray(my_upload.read()), dtype=np.uint8)

        # Use OpenCV to read the file
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.divider()
        st.subheader("Step 2: Some data augmentation demos")

        col1, col2, col3 = st.columns(3)

        with col1:
            utils.do_image_augment(image, 'A.HorizontalFlip(p=1)')
            utils.do_image_augment(image, 'A.Blur(blur_limit=100, p=1)')
            utils.do_image_augment(image, 'A.ToGray(p=1)')

        with col2:
            utils.do_image_augment(image, 'A.VerticalFlip(p=1)')
            utils.do_image_augment(image, 'A.OpticalDistortion(p=1)')
            utils.do_image_augment(image, 'A.RandomBrightnessContrast(brightness_limit=0.8, contrast_limit=0.8, p=1)')

        with col3:
            utils.do_image_augment(image, 'A.ShiftScaleRotate(p=1)')
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
            st.image(augmented_image, caption="augmented Image", use_column_width=False)


if __name__ == "__main__":
    main()
