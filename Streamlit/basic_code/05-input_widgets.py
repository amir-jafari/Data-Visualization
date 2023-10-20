import streamlit as st
from datetime import time
import datetime
import numpy as np
import pandas as pd
import random

# %%--------------------------------------------------------------------------------------------------------------------
st.header("Input widgets")
st.write("With widgets, Streamlit allows you to bake interactivity directly into your apps with buttons, sliders, text inputs, and more.")

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Button***")

code = """
st.button("Reset", type="primary")
if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Download button***")

st.write("***Download an image***")
code = '''
with open("../static/flower.png", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
          )
'''

st.code(code, language='python')
exec(code)

st.write('\n\n')
st.write("***Download a large DataFrame as a CSV***")

code = '''
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

my_large_df = pd.DataFrame(
   {
       "col1": list(range(20)) * 3,
       "col2": np.random.randn(60),
       "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,
   }
)

csv = convert_df(my_large_df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)
'''

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Link button***")

code = '''
st.link_button("Go to gallery", "https://streamlit.io/gallery")
'''

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Checkbox***")

code = '''
agree = st.checkbox('I agree')

if agree:
    st.write('Great!')
'''

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Toggle widget***")

code = '''
on = st.toggle('Activate feature')

if on:
    st.write('Feature activated!')
'''

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Radio***")

code = '''
genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
    captions = ["Laugh out loud.", "Get the popcorn.", "Never stop learning."],
    index=None,
)

st.write("You selected:", genre)
'''

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Selectbox***")

code = '''
option = st.selectbox(
   "How would you like to be contacted?",
   ("Email", "Home phone", "Mobile phone"),
   index=None,
   placeholder="Select contact method...",
)

st.write('You selected:', option)
'''

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Multiselect***")

code = '''
options = st.multiselect(
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])

st.write('You selected:', options)
'''

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Slider***")

st.write("***A simple range slider***")
code = '''
values = st.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)
'''

st.code(code, language='python')
exec(code)


st.markdown("##")
st.write("***A range time slider***")

code = '''
appointment = st.slider(
    "Schedule your appointment:",
    value=(time(11, 30), time(12, 45)))
st.write("You're scheduled for:", appointment)
'''

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Select slider***")

code = '''
start_color, end_color = st.select_slider(
    'Select a range of color wavelength',
    options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'],
    value=('red', 'blue'))
st.write('You selected wavelengths between', start_color, 'and', end_color)
'''

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Text input***")

code = '''
title = st.text_input('Movie title', 'Life of Brian')
st.write('The current movie title is', title)

number = st.number_input("Insert a number", value=None, placeholder="Type a number...")
st.write('The current number is ', number)
'''

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Text area***")

code = '''
txt = st.text_area(
    "Text to analyze",
    "It was the best of times, it was the worst of times, it was the age of "
    "wisdom, it was the age of foolishness, it was the epoch of belief, it "
    "was the epoch of incredulity, it was the season of Light, it was the "
    "season of Darkness, it was the spring of hope, it was the winter of "
    "despair, (...)",
    )

st.write(f'You wrote {len(txt)} characters.')
'''

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Date-time input***")

code = '''
d = st.date_input("When's your birthday", value=None)
st.write('Your birthday is:', d)

today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

d = st.date_input(
    "Select your vacation for next year",
    (jan_1, datetime.date(next_year, 1, 7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)
d

t = st.time_input('Set an alarm for', datetime.time(8, 45))
st.write('Alarm is set for', t)
'''

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***File uploader***")

code = '''
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)
'''

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Color picker***")

code = '''
color = st.color_picker('Pick A Color', '#00f900')
st.write('The current color is', color)
'''

st.code(code, language='python')
exec(code)
