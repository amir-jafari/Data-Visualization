import streamlit as st

st.subheader("***Text input***")

code = '''
title = st.text_input('Movie title', 'Life of Brian')
st.write('The current movie title is', title)

number = st.number_input("Insert a number", value=None, placeholder="Type a number...")
st.write('The current number is ', number)
'''

st.code(code, language='python')
exec(code)
