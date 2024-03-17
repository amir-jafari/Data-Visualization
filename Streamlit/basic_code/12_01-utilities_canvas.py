import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
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

# Do something interesting with the image data and paths
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)
if canvas_result.json_data is not None:
    st.dataframe(pd.json_normalize(canvas_result.json_data["objects"]))