import streamlit as st

st.subheader("***Color picker***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    color = st.color_picker('Pick A Color', '#00f900')
    st.write('The current color is', color)
