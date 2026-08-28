import streamlit as st
import numpy as np
import pandas as pd


# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Line chart***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    chart_data = pd.DataFrame(
        np.random.randint(low=0, high=100, size=(20, 3)),
        columns =['a', 'b', 'c'])

    st.line_chart(chart_data)
