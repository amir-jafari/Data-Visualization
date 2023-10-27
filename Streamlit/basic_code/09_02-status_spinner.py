import streamlit as st
import time

st.subheader("***Spinner***")
st.write("Temporarily displays a message while executing a block of code.")

code = """
with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')
"""

st.code(code, language='python')

exec(code)
