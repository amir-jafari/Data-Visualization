import streamlit as st
import time

st.subheader("***Status Container***")
st.write("Insert a status container to display output from long-running tasks.")

code = """
with st.status("Downloading data..."):
    st.write("Searching for data...")
    time.sleep(2)
    st.write("Found URL.")
    time.sleep(1)
    st.write("Downloading data...")
    time.sleep(1)

st.button('Rerun')
"""

st.code(code, language='python')

exec(code)
