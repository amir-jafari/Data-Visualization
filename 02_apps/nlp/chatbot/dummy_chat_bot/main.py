"""
Dummy chatbot -- the echo bot plus a typing effect and canned replies.

What it shows:
    * st.empty() as a placeholder you overwrite repeatedly, which is how the
      word-by-word "typing" animation works underneath
    * still no model: the reply is picked at random from a list

The next demo up (open_source_chatbot) does the same effect with
st.write_stream(), the shortcut for exactly this pattern -- see
01_basics/07_chat/03_write_stream.py.

Reference: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

    streamlit run 02_apps/nlp/chatbot/dummy_chat_bot/main.py
"""

import streamlit as st
import random
import time

REPLIES = [
    "Hello there! How can I assist you today?",
    "Hi, human! Is there anything I can help you with?",
    "Do you need help?",
]


def main():
    st.title("Simple chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # One placeholder, overwritten once per word -- that is the whole trick.
            message_placeholder = st.empty()
            full_response = ""

            for chunk in random.choice(REPLIES).split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")   # ▌ = fake cursor

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
