import streamlit as st

st.subheader("***Selectbox***")

code = '''
option = st.selectbox(
   "How would you like to be contacted?",
   ("Email", "Home phone", "Mobile phone"),
   index=None,
   placeholder="Select contact method...",
)

st.write('You selected:', option)
'''

st.code(code, language='python')
exec(code)
