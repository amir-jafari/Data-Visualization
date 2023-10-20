import streamlit as st
import pandas as pd
from datetime import datetime, date, time

# %%--------------------------------------------------------------------------------------------------------------------
st.header("***Data elements***")
st.write("Use to display and interact with raw data.")

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Data editor***")
st.write("Edit dataframes and many other data structures in a table-like UI")

code = """
df = pd.DataFrame(
    [
       {"command": "st.selectbox", "rating": 4, "is_widget": True},
       {"command": "st.balloons", "rating": 5, "is_widget": False},
       {"command": "st.time_input", "rating": 3, "is_widget": True},
   ]
)

# allow the user to add and delete rows by setting num_rows to "dynamic"
edited_df = st.data_editor(df, num_rows="dynamic")

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
"""

st.code(code, language='python')

exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Column configuration***")
st.write("Configure the display and editing behavior of dataframes and data editors")
st.write("The columns, from left to right, are ***text, number, checkbox, selectbox, and datetime***")

code = """
data_df = pd.DataFrame(
    {
        "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
        "price": [20, 950, 250, 500],
        "favorite": [True, False, False, True],
        "category": ["📊 Data Exploration", "📈 Data Visualization", "🤖 LLM", "📊 Data Exploration"],
        "appointment": [datetime(2024, 2, 5, 12, 30), datetime(2023, 11, 10, 18, 0), datetime(2024, 3, 11, 20, 10), datetime(2023, 9, 12, 3, 0)]
    }
)

st.data_editor(
    data_df,
    column_config={
        "widgets": st.column_config.TextColumn(
            "Widgets",
            help="Streamlit **widget** commands 🎈",
            default="st.",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        ),
        "price": st.column_config.NumberColumn(
            "Price (in USD)",
            help="The price of the product in USD",
            min_value=0,
            max_value=1000,
            step=1,
            format="$%d",
        ),
        "favorite": st.column_config.CheckboxColumn(
            "Your favorite?",
            help="Select your **favorite** widgets",
            default=False,
        ),
        "category": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="medium",
            options=[
                "📊 Data Exploration",
                "📈 Data Visualization",
                "🤖 LLM",
            ],
            required=True,
        ),
        "appointment": st.column_config.DatetimeColumn(
            "Appointment",
            min_value=datetime(2023, 6, 1),
            max_value=datetime(2025, 1, 1),
            format="D MMM YYYY, h:mm a",
            step=60,
        ),
    },
    hide_index=True,
)
"""

exec(code)

expander = st.expander("Click to view code", expanded=False)
with expander:
    st.code(code, language='python')


# %%--------------------------------------------------------------------------------------------------------------------
st.write("\n\n")
st.write("\n\n")
st.write("The columns, from left to right, are ***date, time, list, and link***")

code = """
data_df = pd.DataFrame(
    {
        "birthday": [
            date(1980, 1, 1),
            date(1990, 5, 3),
            date(1974, 5, 19),
            date(2001, 8, 17),
        ],
        "appointment": [
            time(12, 30),
            time(18, 0),
            time(9, 10),
            time(16, 25),
        ],
        "sales": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
        "apps": [
            "https://roadmap.streamlit.app",
            "https://extras.streamlit.app",
            "https://issues.streamlit.app",
            "https://30days.streamlit.app",
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "birthday": st.column_config.DateColumn(
            "Birthday",
            min_value=date(1900, 1, 1),
            max_value=date(2005, 1, 1),
            format="DD.MM.YYYY",
            step=1,
        ),
        "appointment": st.column_config.TimeColumn(
            "Appointment",
            min_value=time(8, 0, 0),
            max_value=time(19, 0, 0),
            format="hh:mm a",
            step=60,
        ),
        "sales": st.column_config.ListColumn(
            "Sales (last 6 months)",
            help="The sales volume in the last 6 months",
            width="medium",
        ),
        "apps": st.column_config.LinkColumn(
            "Trending apps",
            help="The top trending Streamlit apps",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
        )
    },
    hide_index=True,
)
"""

exec(code)

expander = st.expander("Click to view code", expanded=False)
with expander:
    st.code(code, language='python')


# %%--------------------------------------------------------------------------------------------------------------------
st.write("\n\n")
st.write("\n\n")
st.write("The columns, from left to right, are ***image, line chart, bar chart, and progress***")

code = """
data_df = pd.DataFrame(
    {
        "apps": [
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/ef9a7627-13f2-47e5-8f65-3f69bb38a5c2/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/31b99099-8eae-4ff8-aa89-042895ed3843/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/6a399b09-241e-4ae7-a31f-7640dc1d181e/Home_Page.png",
        ],
        "sales": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
        "sales2": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
        "sales3": [200, 550, 1000, 80],
    }
)

st.data_editor(
    data_df,
    column_config={
        "apps": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots"
        ),
        "sales": st.column_config.LineChartColumn(
            "Sales (last 6 months)",
            width="medium",
            help="The sales volume in the last 6 months",
            y_min=0,
            y_max=100,
        ),
        "sales2": st.column_config.BarChartColumn(
            "Sales (last 6 months)",
            help="The sales volume in the last 6 months",
            y_min=0,
            y_max=100,
        ),
        "sales3": st.column_config.ProgressColumn(
            "Sales volume",
            help="The sales volume in USD",
            format="$%f",
            min_value=0,
            max_value=1000,
        ),
    },
    hide_index=True,
)
"""

exec(code)

expander = st.expander("Click to view code", expanded=False)
with expander:
    st.code(code, language='python')


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Metrics***")
st.write("Display a metric in big bold font, with an optional indicator of how the metric changed.")


code = """
st.metric(label="Gas price", value=4, delta=-0.5,
    delta_color="inverse")

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Dicts and JSON***")
st.write("Display object or string as a pretty-printed JSON string.")

code = """
st.json({
    'foo': 'bar',
    'baz': 'boz',
    'stuff': [
        'stuff 1',
        'stuff 2',
        'stuff 3',
        'stuff 5',
    ],
})
"""

st.code(code, language='python')
exec(code)
