import streamlit as st
import numpy as np
import pandas as pd

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Bar chart***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    chart_data = pd.DataFrame(
       {
           "col1": list(range(20)) * 3,
           "col2": np.random.randn(60),
           "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,
       }
    )

    st.bar_chart(chart_data, x="col1", y="col2", color="col3")
