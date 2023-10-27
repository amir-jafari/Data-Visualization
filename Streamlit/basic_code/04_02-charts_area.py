import streamlit as st
import numpy as np
import pandas as pd


# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Area chart***")

code = """
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.area_chart(chart_data)"""

st.code(code, language='python')
exec(code)
