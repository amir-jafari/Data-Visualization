# https://medium.com/@sirikrrishna99/automatic-image-captioning-using-streamlit-and-hugging-face-transformers-d3563edb5457
# https://huggingface.co/docs/transformers/main/tasks/image_captioning

import streamlit as st
from transformers import pipeline
from PIL import Image

import utils


def main():
    st.header("Image Caption")
    st.divider()
    st.subheader("Step 1: File uploader")
    model_name = utils.sidebar()

    my_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

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
