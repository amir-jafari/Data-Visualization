import streamlit as st
import numpy as np
import pandas as pd
from vega_datasets import data

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Vega-Lite library chart***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
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
