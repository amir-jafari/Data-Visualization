import streamlit as st
import os

st.subheader("***Video***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('..')

    path = os.getcwd() + os.path.sep + 'static' + os.path.sep + 'myvideo.mp4'

    video_file = open(path, 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)
