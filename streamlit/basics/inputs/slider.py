import streamlit as st
import datetime

st.subheader("***Slider***")

st.write("***A simple range slider***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    values = st.slider(
        'Select a range of values',
        0.0, 100.0, (25.0, 75.0))
    st.write('Values:', values)


st.write("##")

st.write("***A range time slider***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    appointment = st.slider(
        "Schedule your appointment:",
        value=(datetime.time(11, 30), datetime.time(12, 45)))
    st.write("You're scheduled for:", appointment)
