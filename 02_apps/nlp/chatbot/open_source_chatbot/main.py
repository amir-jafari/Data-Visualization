# Reference: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
# https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/
# https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/

import streamlit as st
import random
import time
from utils_gen_ai import gen_ai, side_bar

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils

# The logo lives in S3: s3://dats-dl/ajafari@gwu.edu/streamlit/static/gwu.jpg
left_co, cent_co, last_co = st.columns(3)
with cent_co:
    logo = st.image(s3_utils.read_image('static/gwu.jpg'), width=100)

st.title("NLP Class Chatbot with AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", "👤")):
        st.markdown(message["content"])

side_bar()


# Accept user input
if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Add user message to chat history
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar="👩‍💻"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = gen_ai(context=None, prompt=prompt)
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)




    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})


