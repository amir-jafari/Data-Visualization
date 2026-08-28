import streamlit as st


# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Metrics***")
st.write("Display a metric in big bold font, with an optional indicator of how the metric changed.")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    st.metric(label="Gas price", value=4, delta=-0.5,
        delta_color="inverse")

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")
