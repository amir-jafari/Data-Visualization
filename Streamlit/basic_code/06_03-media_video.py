import streamlit as st
import os

st.subheader("***Video***")

code = """
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')

path = os.getcwd() + os.path.sep + 'static' + os.path.sep + 'myvideo.mp4'

video_file = open(path, 'rb')
video_bytes = video_file.read()

st.video(video_bytes)
"""

st.code(code, language='python')
exec(code)
