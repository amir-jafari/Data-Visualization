import streamlit as st
import numpy as np
import pandas as pd


# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Line chart***")

code = """
chart_data = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(20, 3)),
    columns =['a', 'b', 'c'])

st.line_chart(chart_data)
"""

st.code(code, language='python')
exec(code)
