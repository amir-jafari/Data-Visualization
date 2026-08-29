import streamlit as st

st.subheader("***File uploader***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)
