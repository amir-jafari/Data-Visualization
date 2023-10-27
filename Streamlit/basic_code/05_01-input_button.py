import streamlit as st

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Button***")

st.write("***Regular Button***")
code = """
st.button("Reset", type="primary")
if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')
"""

st.code(code, language='python')
exec(code)

st.write("##")
st.write("***Link button***")
code = '''
st.link_button("Go to gallery", "https://streamlit.io/gallery")
'''

st.code(code, language='python')
exec(code)
