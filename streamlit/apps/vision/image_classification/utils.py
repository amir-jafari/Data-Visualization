import streamlit as st


def sidebar():
    with st.sidebar:
        genre = st.radio(
            "Which model will you want to use?",
            ["google/vit-base-patch16-224"],
            captions=["Use the pretrained model to classify."],
            index=0,
        )
        return genre
