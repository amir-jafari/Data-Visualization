import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data

import random

st.header("Plots - Charts")

st.write("We can output the visualizations using any of the python visualization libraries such as matplotlib, seaborn, plotly, etc. I recommend using seaborn and plotly for better visualization.")
st.write("On top of it, streamlit also has an inbuilt visualization library. We can use st.line_chart(), st.area_chart(), st.bar_chart(), st.pyplot(), st.vega_lite_chart(), st.altair_chart(), st.plotly_chart() to display the charts.")

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Line chart***")

code = """
chart_data = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(20, 3)),
    columns =['a', 'b', 'c'])

st.line_chart(chart_data)
"""

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Area chart***")

code = """
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.area_chart(chart_data)"""

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Bar chart***")

code = """
chart_data = pd.DataFrame(
   {
       "col1": list(range(20)) * 3,
       "col2": np.random.randn(60),
       "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,
   }
)

st.bar_chart(chart_data, x="col1", y="col2", color="col3")
"""

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Scatter chart***")

code = """
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["col1", "col2", "col3"])
chart_data['col4'] = np.random.choice(['A','B','C'], 20)

st.scatter_chart(
    chart_data,
    x='col1',
    y='col2',
    color='col4',
    size='col3',
)
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Pyplot***")

code = """
arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Altair library chart***")

code = """
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

c = (
   alt.Chart(chart_data)
   .mark_circle()
   .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.altair_chart(c, use_container_width=True)
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Vega-Lite library chart***")

code = """
import streamlit as st
from vega_datasets import data

source = data.cars()

chart = {
    "mark": "point",
    "encoding": {
        "x": {
            "field": "Horsepower",
            "type": "quantitative",
        },
        "y": {
            "field": "Miles_per_Gallon",
            "type": "quantitative",
        },
        "color": {"field": "Origin", "type": "nominal"},
        "shape": {"field": "Origin", "type": "nominal"},
    },
}

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Vega-Lite native theme"])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.vega_lite_chart(
        source, chart, theme="streamlit", use_container_width=True
    )
with tab2:
    st.vega_lite_chart(
        source, chart, theme=None, use_container_width=True
    )
"""

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Plotly chart***")

code = """
import plotly.figure_factory as ff

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Scatterplots on maps***")

code = """
df = pd.DataFrame({
    "col1": np.random.randn(1000) / 50 + 37.76,
    "col2": np.random.randn(1000) / 50 + -122.4,
    "col3": np.random.randn(1000) * 100,
    "col4": np.random.rand(1000, 4).tolist(),
})

st.map(df,
    latitude='col1',
    longitude='col2',
    size='col3',
    color='col4')
"""

st.code(code, language='python')
exec(code)
