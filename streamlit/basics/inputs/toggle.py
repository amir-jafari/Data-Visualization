import streamlit as st

st.subheader("***Toggle widget***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    on = st.toggle('Activate feature')

    if on:
        st.write('Feature activated!')
