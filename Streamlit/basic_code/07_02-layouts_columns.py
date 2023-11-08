import streamlit as st

st.subheader("***Columns***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    col1, col2, col3 = st.columns(3)

    with col1:
       st.header("A cat")
       st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
       st.header("A dog")
       st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
       st.header("An owl")
       st.image("https://static.streamlit.io/examples/owl.jpg")
