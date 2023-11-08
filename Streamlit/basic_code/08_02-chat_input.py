import streamlit as st

st.subheader("***Chat input***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    prompt = st.chat_input("Say something")
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")

