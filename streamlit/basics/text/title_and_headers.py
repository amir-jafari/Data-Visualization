import streamlit as st

st.subheader("***Title and headers***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    st.title("This is a title")
    st.header("This is a header")
    st.subheader("This is a subheader")
    st.write("This is the place you can start writing")