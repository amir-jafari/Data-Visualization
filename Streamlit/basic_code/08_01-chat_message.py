import streamlit as st
import numpy as np

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
