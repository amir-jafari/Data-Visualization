"To install stream lit use pip install streamlit"

import streamlit as st
import numpy as np
import pandas as pd
import random
import datetime
from io import StringIO



# Basic building blocks of streamlit


# Display text in the form of a title
st.title("Streamlit 101")


# Display text in the form of a header
st.header("Understanding the basics of streamlit")

st.markdown("""___""")  # to add a horizontal line


# creating a markdown
st.markdown("Streamlit is an open-source Python library that allows developers to create interactive, web-based data applications quickly. It's designed to make data exploration, model prototyping, and creating interactive dashboards intuitive and straightforward.")


st.header("Displaying text using streamlit")

# Creating text elements like headers, subheaders, text, markdown, etc.

st.write("Create the text elements such as headers, subheaders, text, markdown, etc. using st.header(), st.subheader(), st.text(), st.markdown()")
code = """st.title("Body")
st.header("Body")
st.subheader("Body")
st.text("text")
st.markdown("markdown")"""

st.code(code, language='python')

st.subheader("***Display anything using st.write()***")
st.write("This can be a text, a dataframe, a chart, an image, a widget, etc.")

code = """st.write("hello world")"""
st.code(code, language='python')  # to display code


st.subheader("Display without using st.write()")
st.write("If there is a variable, we can directly show it just by writing its name and streamlit will automatically understand its type and display it accordingly")


code = """output_text = "show the variable without calling st.write()"
output_text
"""
st.code(code, language='python')

output_text = "show the variable without calling st.write()"
st.write("***This is an example of not using st.write()***")
output_text

st.divider()

# creating and displaying a dataframe

st.subheader("Working with Dataframes")

st.write("We can create an interactive dataframe using st.dataframe()")
st.write("This dataframe output has an ability sorting and changing the column width in the UI")

code = """df = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(10, 10)),
    columns=('col %d' % i for i in range(10)))

st.dataframe(df)"""

st.code(code, language='python')


df = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(5, 10)),
    columns=('col %d' % i for i in range(10)))

st.dataframe(df)

st.write("st.dataframe() can also be helpful to render dataframe in different styles")

code = """df = pd.DataFrame(
   np.random.randn(5, 10),
   columns=('col %d' % i for i in range(00)))

st.dataframe(df.style.highlight_max(axis=0))"""

st.code(code, language='python')

df = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(5, 10)),
    columns=('col %d' % i for i in range(10)))

st.dataframe(df.style.highlight_max(axis=0))

st.write("In this example we highlight the highest value in each column")

st.write("We can also customize the dataframe to show plots in the cells")

code = """
df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)
st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)"""

st.code(code, language='python')

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)
st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)

st.divider()

st.subheader("Displaying charts using streamlit")

st.write("We can output the visualizations using any of the python visualization libraries such as matplotlib, seaborn, plotly, etc.I recommend using seaborn and plotly for better visualization.")
st.write("On top of it, streamlit also has an inbuilt visualization library. We can use st.line_chart(), st.area_chart(), st.bar_chart(), st.pyplot(), st.vega_lite_chart(), st.altair_chart(), st.plotly_chart() to display the charts")

st.write("***Line chart***")

code = """chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)"""

st.code(code, language='python')

chart_data = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(20, 3)),
    columns =['a', 'b', 'c'])

st.line_chart(chart_data)

st.write("***Area chart***")

code = """chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.area_chart(chart_data)"""

chart_data = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(20, 2)),
    columns=['a', 'b'])

st.area_chart(chart_data)

st.divider()

st.subheader("Creating form elements")

st.write("We can create a button for the user to click on using st.button()")

code = """if st.button('Continue'):
    st.write('hello there')
else:
    st.write('Click to continue')"""
    
st.code(code, language='python')

if st.button('Continue'):
    st.write('hello there')
else:
    st.write('Click to continue')
    
st.write("Based on the condition of the button, we can display an output or run a task")

st.subheader("Checkbox")

code = """agree = st.checkbox('check to agree')

if agree:
    st.write('Great, you have checked the box')
    """
    

st.code(code, language='python')

agree = st.checkbox('check to agree')

if agree:
    st.write('Great, you have checked the box')
    
st.write("Similar to how the button works, we can use the checkbox to display an output or run a task")

st.subheader("Radio button")


code = """page_names = ["Comedy", "Drama", "Documentary"]
genre = st.radio(
    "What's your favorite movie genre",page_names)

st.write("***You have selected:***", genre)

if genre == 'Comedy':
    st.subheader("Here is the list of comedy movies!!")
    st.write("1. The Hangover \n 2. The Dictator \n 3. The Other Guys") 
    
if genre == 'Drama':
    st.header("Here is the list of drama movies!!")
    st.write("1. The Shawshank Redemption \n 2. The Godfather \n 3. The Dark Knight")
    
if genre == 'Documentary':
    st.header("Here is the list of documentary movies!!")
    st.write("1. The Social Dilemma \n 2. The Great Hack \n 3. The Game Changers")"""
    
st.write("We can use the radio button to display an output or run a task based on the selection")

st.code(code, language='python')


page_names = ["Comedy", "Drama", "Documentary"]
genre = st.radio(
    "What's your favorite movie genre",page_names)

st.write("***You have selected:***", genre)

if genre == 'Comedy':
    st.write("***Here is the list of comedy movies!!***")
    st.write("1. The Hangover \n 2. The Dictator \n 3. The Other Guys") 
    
if genre == 'Drama':
    st.write("***Here is the list of drama movies!!***")
    st.write("1. The Shawshank Redemption \n 2. The Godfather \n 3. The Dark Knight")
    
if genre == 'Documentary':
    st.write("***Here is the list of documentary movies!!***")
    st.write("1. The Social Dilemma \n 2. The Great Hack \n 3. The Game Changers")
    
    
st.subheader("Selectbox")

st.write("We can use the selectbox to display an output or run a task based on the selection")

code = """school_list = ["Columbian College of Arts & Sciences","Corcoran School of the Arts & Design",
               "School of Business","Graduate School of Education & Human Development",
               "School of Engineering & Applied Science","School of Medicine & Health Sciences",
               "Elliott School of International Affairs","Milken Institute School of Public Health","GW Law",
               "School of Media & Public Affairs","School of Medicine & Health Sciences","School of Nursing",
               "Graduate School of Political Management"]

option = st.selectbox(
    'In which school do you study in GWU?',school_list)

st.write('***You study in***', option)"""

st.code(code, language='python')

school_list = ["Columbian College of Arts & Sciences","Corcoran School of the Arts & Design",
               "School of Business","Graduate School of Education & Human Development",
               "School of Engineering & Applied Science","School of Medicine & Health Sciences",
               "Elliott School of International Affairs","Milken Institute School of Public Health","GW Law",
               "School of Media & Public Affairs","School of Medicine & Health Sciences","School of Nursing",
               "Graduate School of Political Management"]

option = st.selectbox(
    '***In which school do you study in GWU?***',school_list)

st.write('***You study in :***', option)

st.subheader("Multiselect")

st.write("for tasks which require multiple selection, we can use the multiselect option in streamlit")

code = """color_list = ["Red","Blue","Green","Yellow","Orange","Purple","Pink","Brown","Black","White"]

selection = st.multiselect('Which colors do you like?', color_list)

st.write("You have selected ",len(selection), "colors")
st.write("here are the list of your favorite colors", selection)"""

st.code(code, language='python')

color_list = ["Red","Blue","Green","Yellow","Orange","Purple","Pink","Brown","Black","White"]

selection = st.multiselect('Which colors do you like?', color_list)

st.write("You have selected ",len(selection), "colors")
st.write("here are the list of your favorite colors", selection)


st.subheader("Slider")

st.write("streamlit provides you an option to select a value or a range of values using the slider")

code = """age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')

values = st.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0))
st.write('You have selected a range of: ', values)"""

st.code(code, language='python')

age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')

values = st.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0))
st.write('You have selected a range of: ', values)

st.subheader("Text Input")

st.write("We can use the text input to get the input from the user")

code = """title = st.text_input('Input your Name', 'Pranav Sai')
st.write('Your Name: ', title)"""

st.code(code, language='python')

title = st.text_input('Input your Name', 'Pranav Sai')
st.write('Your Name: ', title)
    
    
st.subheader("date_input")

st.write("for tasks which require date input, we can use the date_input option in streamlit")

code = """d = st.date_input(
    "When\'s your birthday",
    datetime.date(1998, 7, 1))
st.write('Your birthday is:', d)"""

st.code(code, language='python')

d = st.date_input(
    "When\'s your birthday",
    datetime.date(1998, 7, 1))
st.write('Your birthday is:', d)


st.subheader("time_input")
st.write("We will take an example of scheduling a meeting")

code = """d = st.date_input(
    "when would you like to schedule the meeting?",
    datetime.date(2023, 7, 15))
t = st.time_input('Time', datetime.time(8, 45))

st.write('You have scheduled a meeting on', d, 'at', t)"""

st.code(code, language='python')    

d = st.date_input(
    "when would you like to schedule the meeting?",
    datetime.date(2023, 7, 15))
t = st.time_input('Time', datetime.time(8, 45))

st.write('You have scheduled a meeting on', d, 'at', t)

st.divider()

st.subheader("File Uploader")

st.write("we can take an input from the user using the file uploader")

code = """uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)"""
    
st.code(code, language='python')


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

