import streamlit as st

st.subheader("***Radio***")

code = '''
genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
    captions = ["Laugh out loud.", "Get the popcorn.", "Never stop learning."],
    index=None,
)

st.write("You selected:", genre)
'''

st.code(code, language='python')
exec(code)
