"""
Text cleaning -- the preprocessing every NLP project starts with.

What it shows:
    * each step applied one at a time so you can see what it removes:
      lowercasing, punctuation, stopwords, stemming, lemmatising
    * why order matters, and what you lose at each stage

Run this before sentiment_analysis/ or text_classification/ -- it is the step
those two assume you already understand.

    streamlit run 02_apps/nlp/text_cleaning/main.py
"""

import streamlit as st
import utils


def main():
    st.header("Text Cleaning")
    st.divider()
    st.subheader("Step 1: Type the text")

    txt = utils.get_txt()

    st.divider()
    st.subheader("Step 2: Choose the cleaning methods from left side bar")

    selected = utils.sidebar()

    if st.button('Finish typing and choosing', type="primary"):
        if not selected:
            st.error("No text cleaning methods selected")
            st.stop()

        for step, item in enumerate(selected, 3):
            st.divider()
            st.subheader(f"Step {step}: {item[1]}")
            txt = utils.clean(txt, item[0])
            with st.expander("See result", expanded=True):
                st.write(txt)


if __name__ == "__main__":
    main()
