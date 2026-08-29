"""
Chat agents -- the same Bedrock call, steered by a system prompt.

What it shows:
    * a **system prompt** is what turns one model into different "agents":
      the doctor and the patient here are the same model, prompted differently
    * switching persona mid-conversation, and how the history is rebuilt so
      the model sees the new instructions
    * sidebar buttons acting as a toggle via st.session_state

This is the smallest honest version of an "agent": no tools, no memory beyond
the transcript -- just a role. Read api_chatbot/ first.

Needs the [bedrock] block of the repo-root .env -- see s3/README.md.

    streamlit run streamlit/apps/nlp/chatbot/agent_tools/main.py
"""

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
        <span style="color: white; font-size: 40px; font-weight: bold;">M</span>
    </div>
</div>
<h1 style="text-align: center; margin-top: 0;">Medical Chat Agents</h1>
<p style="text-align: center; color: #666; margin-bottom: 30px;">Toggle between Doctor and Patient roles</p>
"""

# The only difference between the two agents is this block of text.
SYSTEM_PROMPTS = {
    "doctor": """You are a knowledgeable and compassionate medical doctor.
Your role is to provide helpful, accurate medical information and advice based on current medical knowledge.
Always be professional, empathetic, and clear in your explanations.
Remember to mention when a patient should seek in-person medical care for proper diagnosis and treatment.
Never provide dangerous or unethical medical advice.
""",
    "patient": """You are a patient seeking medical advice or information.
You have concerns about your health and are looking for guidance.
Ask questions about symptoms, treatments, or general health information.
Be specific about your concerns and provide relevant details when asked.
""",
}

BANNERS = {
    "doctor": "👨‍⚕️ You are currently in the **Doctor** role. Provide medical advice and information.",
    "patient": "🤒 You are currently in the **Patient** role. Ask questions about medical concerns.",
}

DEFAULTS = {"messages": [], "input_key": 0, "temperature": 0.3,
            "top_k": 250, "current_agent": "doctor"}


def sidebar():
    """Role toggle plus model settings. Writes straight to session_state."""
    with st.sidebar:
        st.subheader("Settings")
        st.write("Current Role:")

        col1, col2 = st.columns(2)
        with col1:
            doctor_button = st.button(
                "👨‍⚕️ Doctor", width='stretch',
                type="primary" if st.session_state.current_agent == "doctor" else "secondary")
        with col2:
            patient_button = st.button(
                "🤒 Patient", width='stretch',
                type="primary" if st.session_state.current_agent == "patient" else "secondary")

        for pressed, role in ((doctor_button, "doctor"), (patient_button, "patient")):
            if pressed and st.session_state.current_agent != role:
                st.session_state.current_agent = role
                st.rerun()

        st.divider()

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
            st.session_state.input_key += 1
            st.rerun()


def history_for_api():
    """The system prompt for the current role, then every earlier message.

    Rebuilt from scratch on each turn, so switching role mid-conversation
    re-sends the *new* instructions with the whole transcript.
    """
    history = [{"role": "system",
                "content": SYSTEM_PROMPTS[st.session_state.current_agent]}]

    for message in st.session_state.messages[:-1]:
        converted = {"role": message["role"], "content": message["content"]}
        if converted["role"] == "bot":
            converted["role"] = "assistant"
        history.append(converted)

    return history


def main():
    st.set_page_config(page_title="Doctor-Patient Chat Agents", page_icon="👨‍⚕️")
    st.markdown(HEADER, unsafe_allow_html=True)

    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

    sidebar()
    st.info(BANNERS[st.session_state.current_agent])

    user_input = st.text_input("Message", placeholder="Type your message...",
                               label_visibility="collapsed",
                               key=f"user_input_{st.session_state.input_key}")

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You ({message['agent']}):** {message['content']}")
        else:
            st.markdown(f"**AI:** {message['content']}")

    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input,
                                      "agent": st.session_state.current_agent})

    with st.spinner("Thinking..."):
        ai_response = ask_llm(user_input, history_for_api(),
                              temperature=st.session_state.temperature,
                              top_k=st.session_state.top_k)

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
