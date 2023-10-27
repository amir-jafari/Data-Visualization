import streamlit as st

st.subheader("***Color picker***")

code = '''
color = st.color_picker('Pick A Color', '#00f900')
st.write('The current color is', color)
'''

st.code(code, language='python')
exec(code)
