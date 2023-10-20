import streamlit as st
import numpy as np
from PIL import Image

# %%--------------------------------------------------------------------------------------------------------------------
st.header("Media elements")
st.write("It's easy to embed images, videos, and audio files directly into your Streamlit apps.")


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Image***")

code = """
image = Image.open('../static/flower.png')

st.image(image, caption='A beautiful flower')
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Audio***")

code = """
audio_file = open('../static/myaudio.ogg', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/ogg')

sample_rate = 44100  # 44100 samples per second
seconds = 2  # Note duration of 2 seconds
frequency_la = 440  # Our played note will be 440 Hz
# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
t = np.linspace(0, seconds, seconds * sample_rate, False)
# Generate a 440 Hz sine wave
note_la = np.sin(frequency_la * t * 2 * np.pi)

st.audio(note_la, sample_rate=sample_rate)
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Video***")

code = """
video_file = open('../static/myvideo.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)
"""

st.code(code, language='python')
exec(code)
