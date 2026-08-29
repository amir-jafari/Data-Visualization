import streamlit as st

st.subheader("***Popover***")
st.write(
    "A button that opens a small panel on top of the page. Good for extra "
    "settings you do not want cluttering the main view. The widgets inside "
    "behave exactly like normal ones."
)


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    with st.popover("Chart settings"):
        colour = st.color_picker("Line colour", "#FF4B4B")
        show_grid = st.checkbox("Show grid", value=True)

    st.write("Colour:", colour, "-- grid:", show_grid)

st.info("The values are available outside the popover, even while it is closed.")
