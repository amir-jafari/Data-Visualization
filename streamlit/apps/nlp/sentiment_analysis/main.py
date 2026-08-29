"""
Sentiment analysis -- is this text positive, negative or neutral?

What it shows:
    * the two classic rule-based scorers side by side, no training required:
      TextBlob (polarity/subjectivity) and VADER (tuned for social media)
    * how much you can do before reaching for a neural model

Model: picked in the sidebar. Nothing is downloaded -- both are lexicon-based.

    streamlit run streamlit/apps/nlp/sentiment_analysis/main.py
"""

import streamlit as st
import utils


def main():
    st.header("Sentiment Analysis")
    st.divider()
    st.subheader("Step 1: Type the text")

    txt = utils.get_txt()

    if st.button('Finish typing', type="primary"):
        st.divider()
        st.subheader("Step 2: Clean the text")
        txt = utils.text_pre_processing(txt)
        st.write(txt)

        st.divider()
        st.subheader("Step 3: Get the sentiment")

        result = utils.analyze_sentiment(txt)
        polarity = result.polarity

        score = round(polarity, 2)
        sentiment = 'neutral' if score == 0 else ('positive' if score > 0 else 'negative')

        st.write(f"Sentiment of the text is: ***{sentiment}***, the socre is ***{score}***")

if __name__ == "__main__":
    main()
