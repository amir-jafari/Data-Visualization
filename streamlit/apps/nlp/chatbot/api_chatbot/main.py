"""
API chatbot -- a real LLM through AWS Bedrock.

What it shows:
    * calling a hosted model instead of running one locally (contrast with
      open_source_chatbot/, which downloads several GB)
    * passing the conversation back with every request, because the API is
      stateless -- it only knows what you send it
    * temperature and top_k wired to sidebar sliders

Needs the [bedrock] block of the repo-root .env -- see s3/README.md.

    streamlit run streamlit/apps/nlp/chatbot/api_chatbot/main.py
"""

# %% ----- Imports and Setup
import streamlit as st
import time
# bedrock.py sits one level up, shared by every chatbot demo in this folder.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bedrock import ask_llm

HEADER = """
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
    <div style="background: linear-gradient(90deg, #10a37f, #0e8c6f); border-radius: 50%; width: 80px; height: 80px; display: flex; justify-content: center; align-items: center;">
        <span style="color: white; font-size: 40px; font-weight: bold;">A</span>
    </div>
</div>
<h1 style="text-align: center; margin-top: 0;">Amir GPT</h1>
<p style="text-align: center; color: #666; margin-bottom: 30px;">NLP-powered AI Assistant</p>
"""

DEFAULTS = {"messages": [], "input_key": 0, "temperature": 0.0, "top_k": 250}


# %% ----- Sidebar
def sidebar():
    """Model settings. Returns nothing -- it writes straight to session_state."""
    with st.sidebar:
        st.subheader("Settings")

        st.session_state.temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0,
            value=st.session_state.temperature, step=0.1,
            help="Higher values make output more random, lower values more deterministic")

        st.session_state.top_k = st.slider(
            "Top K", min_value=0, max_value=500,
            value=st.session_state.top_k, step=10,
            help="Limits vocabulary to top K tokens")

        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.input_key += 1     # a fresh key empties the text box
            st.rerun()


def history_for_api():
    """Every earlier message, in the shape the Bedrock call expects."""
    history = []
    for message in st.session_state.messages[:-1]:
        converted = message.copy()
        if converted["role"] == "bot":
            converted["role"] = "assistant"
        history.append(converted)
    return history


# %% ----- App
def main():
    st.set_page_config(page_title="Simple LLM Q&A App", page_icon="🤖")
    st.markdown(HEADER, unsafe_allow_html=True)

    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

    sidebar()

    user_input = st.text_input("Message", placeholder="Ask anything...",
                               label_visibility="collapsed",
                               key=f"user_input_{st.session_state.input_key}")

    for message in st.session_state.messages:
        who = "You" if message["role"] == "user" else "AI"
        st.markdown(f"**{who}:** {message['content']}")

    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        ai_response = ask_llm(user_input, history_for_api(),
                              temperature=st.session_state.temperature,
                              top_k=st.session_state.top_k)

    # Type the answer out one word at a time -- see dummy_chat_bot/ for the trick.
    message_placeholder = st.empty()
    full_response = ""
    for chunk in ai_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        message_placeholder.markdown(f"**AI:** {full_response}▌")
    message_placeholder.markdown(f"**AI:** {full_response}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.input_key += 1
    st.rerun()


if __name__ == "__main__":
    main()
