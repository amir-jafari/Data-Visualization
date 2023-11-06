import streamlit as st
import utils
from transformers import pipeline


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

        hate_speech_detector = pipeline("text-classification", model=model_name)

        # Perform hate speech detection
        result = hate_speech_detector(txt)[0]
        st.write(f"The label of the result is **{result['label']}**, and the score is **{result['score']:.2f}**")


if __name__ == "__main__":
    main()
