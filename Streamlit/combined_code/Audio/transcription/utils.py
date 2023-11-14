import streamlit as st


def sidebar():
    with st.sidebar:
        genre = st.radio(
            "Choose your model",
            ["facebook/wav2vec2-base-960h"],
            index=0,
        )
        return genre
