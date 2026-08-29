import streamlit as st

st.subheader("***Selectbox***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    option = st.selectbox(
       "How would you like to be contacted?",
       ("Email", "Home phone", "Mobile phone"),
       index=None,
       placeholder="Select contact method...",
    )

    st.write('You selected:', option)
