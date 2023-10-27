import streamlit as st

st.subheader("***Chat input***")

code = """
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
"""

st.code(code, language='python')

exec(code)

