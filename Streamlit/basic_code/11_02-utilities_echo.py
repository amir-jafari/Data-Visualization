import streamlit as st


st.subheader("***Echo***")
st.write('Use in a with block to draw some code on the app, then execute it.')

code = """
with st.echo():
    st.write('This code will be printed')
"""

st.code(code, language='python')

st.divider()
st.write("The result of the above code is as follows:")

with st.echo():
    st.write('This code will be printed')
