import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Altair library chart***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    c = (
       alt.Chart(chart_data)
       .mark_circle()
       .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
    )

    st.altair_chart(c, use_container_width=True)

