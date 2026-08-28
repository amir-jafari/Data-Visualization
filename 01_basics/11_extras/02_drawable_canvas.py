import streamlit as st
import pandas as pd

st.subheader("***Drawable canvas***")
st.write(
    "Streamlit's widgets are not the limit. **Custom components** are built by "
    "the community, installed with pip, and used like any other `st.` call. "
    "This one gives you a canvas you can draw on."
)

# Not part of Streamlit itself -- it ships separately, so say so clearly
# instead of failing with a traceback.
try:
    from streamlit_drawable_canvas import st_canvas
except ModuleNotFoundError:
    st.warning("This lesson needs an extra package: **streamlit-drawable-canvas**")
    st.code("pip install streamlit-drawable-canvas", language="bash")
    st.stop()

# %%--------------------------------------------------------------------------------------------------------------------
# Create a canvas with size, color, and other options for interactivity
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=2,
    stroke_color='#e00',
    background_color="#eee",
    width=500,
    height=500,
    drawing_mode="point",
    key="canvas",
)

# The component hands back what you drew, both as pixels and as objects.
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)
if canvas_result.json_data is not None:
    st.dataframe(pd.json_normalize(canvas_result.json_data["objects"]))
