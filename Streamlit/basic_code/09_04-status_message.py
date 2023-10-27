import streamlit as st

st.subheader("***Message***")
st.write("Display status messages.")

code = """
st.error('This is an error', icon="🚨")

st.warning('This is a warning', icon="⚠️")

st.info('This is a purely informational message', icon="ℹ️")

st.success('This is a success message!', icon="✅")

e = RuntimeError('This is an exception of type RuntimeError')
st.exception(e)
"""

st.code(code, language='python')

exec(code)
