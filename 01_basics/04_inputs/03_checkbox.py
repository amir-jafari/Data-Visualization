import streamlit as st

st.subheader("***Checkbox***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    agree = st.checkbox('I agree')

    if agree:
        st.write('Great!')
