import streamlit as st
import numpy as np
import pandas as pd

st.subheader("***Vega-Lite library chart***")
st.write(
    "`st.altair_chart` builds the chart in Python. `st.vega_lite_chart` skips "
    "that and takes the **Vega-Lite spec directly as a dictionary** — the same "
    "JSON grammar Altair generates under the hood."
)

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    # A small cars-style dataset, built here so the lesson needs no extra package.
    rng = np.random.default_rng(0)
    origins = rng.choice(["USA", "Europe", "Japan"], 150)
    horsepower = rng.normal(120, 35, 150).clip(45, 240)

    source = pd.DataFrame({
        "Horsepower": horsepower,
        # heavier engines burn more fuel, plus some noise
        "Miles_per_Gallon": (48 - 0.15 * horsepower + rng.normal(0, 3, 150)).clip(9, 46),
        "Origin": origins,
    })

    # This dict *is* the chart. No Python chart objects involved.
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
            source, chart, theme="streamlit", width='stretch'
        )
    with tab2:
        st.vega_lite_chart(
            source, chart, theme=None, width='stretch'
        )
