import streamlit as st
import numpy as np
import pandas as pd
import random
# %%--------------------------------------------------------------------------------------------------------------------

st.subheader("Plots - Charts")

st.write("We can output the visualizations using any of the python visualization libraries such as matplotlib, seaborn, plotly, etc. I recommend using seaborn and plotly for better visualization.")
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