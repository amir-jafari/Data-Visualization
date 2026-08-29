import streamlit as st

st.subheader("***Multiselect***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    options = st.multiselect(
        'What are your favorite colors',
        ['Green', 'Yellow', 'Red', 'Blue'],
        ['Yellow', 'Red'])

    st.write('You selected:', options)
