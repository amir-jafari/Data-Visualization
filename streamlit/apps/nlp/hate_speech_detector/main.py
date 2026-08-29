"""
Hate speech detector -- classify a piece of text as hateful or not.

What it shows:
    * the smallest useful shape for a text-classification app: text in, label out
    * @st.cache_resource, so the model is downloaded once and not on every rerun

Model: picked in the sidebar.

    streamlit run streamlit/apps/nlp/hate_speech_detector/main.py
"""

import streamlit as st
import utils
from transformers import pipeline


@st.cache_resource(show_spinner="Loading the model...")
def load_pipeline(model_name):
    """Load once and reuse. Keyed on model_name, so switching models reloads."""
    return pipeline("text-classification", model=model_name)


def main():
    st.header("Hate Speech Detector")
    st.divider()
    st.subheader("Step 1: Type the text")

    model_name = utils.sidebar()
    txt = utils.get_txt()

    if st.button('Finish typing', type="primary"):
        st.divider()
        st.subheader("Step 2: Choose a model from left side bar")

        if not model_name:
            st.stop()

        st.write(f'The model you are using is {model_name}')

        st.divider()
        st.subheader("Step 3: Detect if it's hate speech")

        detector = load_pipeline(model_name)
        result = detector(txt)[0]
        st.write(f"The label of the result is **{result['label']}**, and the score is **{result['score']:.2f}**")


if __name__ == "__main__":
    main()
