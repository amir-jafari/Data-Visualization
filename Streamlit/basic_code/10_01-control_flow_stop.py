import streamlit as st

st.subheader("***Stop***")
st.write("Stops execution immediately.")

code = """
name = st.text_input('Name')
if not name:
  st.warning('Please input a name.')
  st.stop()
st.success('Thank you for inputting a name.')
"""

st.code(code, language='python')

exec(code)
