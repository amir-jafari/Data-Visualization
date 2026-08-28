import streamlit as st
import numpy as np
import pandas as pd


# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Area chart***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.area_chart(chart_data)
