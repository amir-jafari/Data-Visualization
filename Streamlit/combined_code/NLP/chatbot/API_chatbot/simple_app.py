# %% ----- Imports and Setup
import streamlit as st
import json
import time
from Streamlit.combined_code.NLP.chatbot.Agents.utils_gen_ai_api import invoke_llm_api

st.set_page_config(page_title="Simple LLM Q&A App", page_icon="🤖")

st.markdown("""
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
    <div style="background: linear-gradient(90deg, #10a37f, #0e8c6f); border-radius: 50%; width: 80px; height: 80px; display: flex; justify-content: center; align-items: center;">
        <span style="color: white; font-size: 40px; font-weight: bold;">A</span>
    </div>
</div>
<h1 style="text-align: center; margin-top: 0;">Amir GPT</h1>
<p style="text-align: center; color: #666; margin-bottom: 30px;">NLP-powered AI Assistant</p>
""", unsafe_allow_html=True)

# %% ----- Title and Description

# %% ----- Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.0
if "top_k" not in st.session_state:
    st.session_state.top_k = 250
if "processing_response" not in st.session_state:
    st.session_state.processing_response = False

def reset_input():
    st.session_state.input_key += 1

# %% ----- Sidebar
with st.sidebar:
    st.subheader("Settings")

    st.session_state.temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.1, 
                                            help="Higher values make output more random, lower values more deterministic")

    st.session_state.top_k = st.slider("Top K", min_value=0, max_value=500, value=st.session_state.top_k, step=10,
                                      help="Limits vocabulary to top K tokens")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        reset_input()
        st.rerun()

# %% ----- User Interface Elements
user_input = st.text_input("", placeholder="Ask anything...", key=f"user_input_{st.session_state.input_key}")

# %% ----- Conversation Display
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**AI:** {message['content']}")

# %% ----- Process User Input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    st.session_state.processing_response = True

    conversation_history = []
    for message in st.session_state.messages[:-1]:
        converted_message = message.copy()
        if converted_message["role"] == "bot":
            converted_message["role"] = "assistant"
        conversation_history.append(converted_message)

    with st.spinner("Thinking..."):
        try:
            response_str = invoke_llm_api(user_input, conversation_history, 
                                         temperature=st.session_state.temperature,
                                         top_k=st.session_state.top_k)

            if response_str:
                response_json = json.loads(response_str)

                if 'content' in response_json:
                    ai_response = response_json['content'][0]['text']
                else:
                    ai_response = "Sorry, I couldn't understand the response from the AI."
            else:
                ai_response = "Sorry, I couldn't get a response from the AI. Please try again."
        except Exception as e:
            ai_response = f"Sorry, I encountered an error: {str(e)}"

    message_placeholder = st.empty()
    full_response = ""

    for chunk in ai_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        message_placeholder.markdown(f"**AI:** {full_response}▌")

    message_placeholder.markdown(f"**AI:** {full_response}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.session_state.processing_response = False

    reset_input()

    st.rerun()
