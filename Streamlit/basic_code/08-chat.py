import streamlit as st
import numpy as np
import pandas as pd

import random

# %%--------------------------------------------------------------------------------------------------------------------
st.header("Chat elements")
st.write("Streamlit provides a few commands to help you build conversational apps. These chat elements are designed to be used in conjunction with each other, but you can also use them separately.")

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Chat message***")

st.write("Use with notation to insert any element into an expander")
code = """
with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))
"""

st.code(code, language='python')
exec(code)


st.write("##")
st.write("Or just call methods directly in the returned objects")
code = """
message = st.chat_message("assistant")
message.write("Hello human")
message.bar_chart(np.random.randn(30, 3))
"""

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Chat input***")

code = """
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
"""

st.code(code, language='python')

exec(code)

