import streamlit as st
import os
import numpy as np

st.subheader("***Audio***")

code = """
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')

path = os.getcwd() + os.path.sep + 'static' + os.path.sep + 'myaudio.ogg'

audio_file = open(path, 'rb')
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
