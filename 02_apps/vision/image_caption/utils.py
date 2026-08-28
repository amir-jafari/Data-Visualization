import streamlit as st


def sidebar():
    with st.sidebar:
        genre = st.radio(
            "Which model will you want to use?",
            ["ydshieh/vit-gpt2-coco-en", "Salesforce/blip-image-captioning-base"],
            # captions=["Use the pretrained model1 for image captioning."],
            index=0,
        )
        return genre
