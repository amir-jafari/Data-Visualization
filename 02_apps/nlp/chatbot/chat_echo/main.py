"""
Echo bot -- the chat loop and nothing else. Start here.

What it shows:
    * st.chat_input / st.chat_message -- the two pieces every chat app needs
    * keeping the conversation in st.session_state, because Streamlit re-runs
      the whole script on every message and a plain list would be wiped

The bot has no intelligence at all: it repeats what you type. That is the
point -- once this loop is clear, the other chatbots only change what
produces the reply.

The `:=` walrus operator (Python 3.8+) assigns *and* returns in one
expression, so `if prompt := st.chat_input(...)` means "read the input, and
carry on only if the user actually typed something".

Reference: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

    streamlit run 02_apps/nlp/chatbot/chat_echo/main.py
"""

import streamlit as st


def main():
    st.title("Echo Bot")

    # The history has to live in session_state to survive the next re-run.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Re-draw the whole conversation every run -- Streamlit starts from a blank page.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = f"Echo: {prompt}"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
