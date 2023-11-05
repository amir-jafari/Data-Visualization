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

        sentiment = utils.analyze_sentiment(txt)

        st.write(f"Sentiment of the text is: {sentiment}")

if __name__ == "__main__":
    main()
