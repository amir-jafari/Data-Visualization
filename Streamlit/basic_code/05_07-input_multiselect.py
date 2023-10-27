import streamlit as st

st.subheader("***Multiselect***")

code = '''
options = st.multiselect(
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])

st.write('You selected:', options)
'''

st.code(code, language='python')
exec(code)
