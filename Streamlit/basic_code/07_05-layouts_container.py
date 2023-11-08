import streamlit as st
import numpy as np

st.subheader("***Container***")
st.write("Insert a multi-element container.")
st.write("Inserts an invisible container into your app that can be used to hold multiple elements. This allows you to, for example, insert multiple elements into your app out of order.")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    with st.container():
       st.write("This is inside the container")

       # You can call any Streamlit command, including custom components:
       st.bar_chart(np.random.randn(50, 3))

    st.write("This is outside the container")
