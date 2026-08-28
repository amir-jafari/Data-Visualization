import streamlit as st
import numpy as np

# --- make Streamlit/s3_utils.py importable from any sub-folder ----------------
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents
                            if (p / "s3_utils.py").is_file())))
import s3_utils

st.subheader("***Audio***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    # s3://dats-dl/ajafari@gwu.edu/streamlit/static/myaudio.ogg
    # read_bytes() stops the app with a "keys need updating" message if S3 refuses us.
    audio_bytes = s3_utils.read_bytes('static/myaudio.ogg')

    st.audio(audio_bytes, format='audio/ogg')

    sample_rate = 44100  # 44100 samples per second
    seconds = 2  # Note duration of 2 seconds
    frequency_la = 440  # Our played note will be 440 Hz
    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, seconds * sample_rate, False)
    # Generate a 440 Hz sine wave
    note_la = np.sin(frequency_la * t * 2 * np.pi)

    st.audio(note_la, sample_rate=sample_rate)

st.caption(f"Source: {s3_utils.uri('static/myaudio.ogg')}")
