import streamlit as st

st.subheader("***Select slider***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    start_color, end_color = st.select_slider(
        'Select a range of color wavelength',
        options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'],
        value=('red', 'blue'))
    st.write('You selected wavelengths between', start_color, 'and', end_color)
