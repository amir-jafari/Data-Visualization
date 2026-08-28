import streamlit as st
import numpy as np
import pandas as pd


# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Scatter chart***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["col1", "col2", "col3"])
    chart_data['col4'] = np.random.choice(['A','B','C'], 20)

    st.scatter_chart(
        chart_data,
        x='col1',
        y='col2',
        color='col4',
        size='col3',
    )
