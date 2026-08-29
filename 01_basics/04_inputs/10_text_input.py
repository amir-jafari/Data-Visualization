import streamlit as st

st.subheader("***Text input***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    title = st.text_input('Movie title', 'Life of Brian')
    st.write('The current movie title is', title)
