import streamlit as st
from PIL import Image
import os

# %%--------------------------------------------------------------------------------------------------------------------
st.header("Media elements")
st.write("It's easy to embed images, videos, and audio files directly into your Streamlit apps.")


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Image***")

code = """
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')

path = os.getcwd() + os.path.sep + 'static' + os.path.sep + 'flower.png'

image = Image.open(path)

st.image(image, caption='A beautiful flower')
"""

st.code(code, language='python')
exec(code)
