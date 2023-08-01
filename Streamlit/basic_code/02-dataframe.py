import streamlit as st
import numpy as np
import pandas as pd
import random
# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Display DataFrame***")
st.write("This variable can be any data format.")
st.divider()
# %%--------------------------------------------------------------------------------------------------------------------
df = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(5, 10)),
    columns=('col %d' % i for i in range(10)))

st.dataframe(df)
st.divider()
# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Display Highlighted DataFrame***")
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
st.divider()
# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Advanced Plotting in DataFrame***")
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
# %%--------------------------------------------------------------------------------------------------------------------
