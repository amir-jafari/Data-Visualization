import streamlit as st

st.subheader("***Checkbox***")

code = '''
agree = st.checkbox('I agree')

if agree:
    st.write('Great!')
'''

st.code(code, language='python')
exec(code)
