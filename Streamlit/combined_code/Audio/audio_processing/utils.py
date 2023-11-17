import streamlit as st


def sidebar(audio_process_lst):
    with st.sidebar:
        genre = st.radio(
            "Choose the audio processing methods",
            audio_process_lst,
            index=None,
        )
        return genre
