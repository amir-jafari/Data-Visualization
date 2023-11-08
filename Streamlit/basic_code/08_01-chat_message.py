import streamlit as st
import numpy as np

st.subheader("***Chat message***")

st.write("Use with notation to insert any element into an expander")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    with st.chat_message("user"):
        st.write("Hello 👋")
        st.line_chart(np.random.randn(30, 3))


st.write("##")
st.write("Or just call methods directly in the returned objects")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    message = st.chat_message("assistant")
    message.write("Hello human")
    message.bar_chart(np.random.randn(30, 3))
