import streamlit as st
from io import BytesIO
import albumentations as A


def sidebar():
    with st.sidebar:
        st.write("Which date augmentation methods do you want to use?")
        # Define a list of options
        options = [
            (A.RandomRotate90(), "A.RandomRotate90()"),
            (A.ShiftScaleRotate(p=0.6), "A.ShiftScaleRotate()"),
            (A.Transpose(), "A.Transpose()"),
            (A.MotionBlur(p=.6), "A.MotionBlur()",),
            (A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.6), "A.ShiftScaleRotate()"),
            (A.OpticalDistortion(p=0.8), "A.OpticalDistortion()"),
            (A.Sharpen(), "A.Sharpen()",),
            (A.HueSaturationValue(p=0.6), "A.HueSaturationValue()"),
            # (A.CenterCrop(p=0.5, height=106, width=158), "A.CenterCrop()"),
        ]

        # Create a dictionary to hold the selection status of each option
        selected_options = {}

        for option in options:
            # Use st.checkbox for each option
            selected = st.checkbox(option[1], key=option[0], value=True)
            selected_options[option] = selected

        # print('selected_options', selected_options)
        # Filter the selected options
        selected = [option for option, selected in selected_options.items() if selected]

        return selected


@st.cache_data
def do_image_augment(image, transform_str):
    # Evaluate the string as Python code
    transform = eval(transform_str)
    augmented_image = transform(image=image)['image']
    st.image(augmented_image, caption=transform_str, use_column_width=True)


def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im
