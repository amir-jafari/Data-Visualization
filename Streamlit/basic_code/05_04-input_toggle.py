import streamlit as st

st.subheader("***Toggle widget***")

code = '''
on = st.toggle('Activate feature')

if on:
    st.write('Feature activated!')
'''

st.code(code, language='python')
exec(code)
