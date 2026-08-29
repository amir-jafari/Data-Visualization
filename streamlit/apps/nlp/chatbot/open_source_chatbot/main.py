"""
Open-source chatbot -- a real LLM, running locally, no API and no AWS keys.

What it shows:
    * a HuggingFace model driven through LangChain (see utils_gen_ai.py)
    * @st.cache_resource, so the multi-GB model loads once instead of on
      every rerun -- without it this page is unusably slow
    * st.write_stream() for the typing effect

The model is several GB and downloads on first use. If you only want the
chat mechanics, read chat_echo/ first.

References:
    https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
    https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/

    streamlit run streamlit/apps/nlp/chatbot/open_source_chatbot/main.py
"""

import streamlit as st
import time
from utils_gen_ai import gen_ai, side_bar

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils


def stream_words(text, delay=0.05):
    """Yield `text` one word at a time, so st.write_stream can type it out."""
    for word in text.split():
        yield word + " "
        time.sleep(delay)


def main():
    # The logo lives in S3: s3://dats-dl/ajafari@gwu.edu/streamlit/static/gwu.jpg
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image(s3_utils.read_image('static/gwu.jpg'), width=100)

    st.title("NLP Class Chatbot with AI")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar", "👤")):
            st.markdown(message["content"])

    side_bar()

    if prompt := st.chat_input("How can I help you?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👩‍💻"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            answer = gen_ai(context=None, prompt=prompt)
            # write_stream draws each piece as it arrives and hands back the full text
            full_response = st.write_stream(stream_words(answer))

        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
