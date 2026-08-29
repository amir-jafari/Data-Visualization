"""
Plotly -- hover, zoom and pan, from a familiar API.

What it shows:
    * plotly.express: one line per chart, like seaborn
    * hover text carrying fields that are NOT in the x/y position
    * a written-out HTML file you can open, email, or embed in Streamlit
    * the same figure, but static, for when it goes in a document

In Streamlit these go straight into st.plotly_chart(fig) -- see
streamlit/basics/charts/plotly_chart.py.

Run it:
    python viz/basics/interactive/plotly_basics.py
    then open the .html files it prints
"""

import sys
from pathlib import Path

import plotly.express as px

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save_html, sales, students        # noqa: E402

# --- 1. hover is the reason to reach for plotly ----------------------------
data = students()
figure = px.scatter(
    data, x="hours", y="score", color="group",
    color_discrete_map={"morning": "#0072B2", "evening": "#D55E00"},
    # These appear on hover but occupy no space on the chart -- the one thing
    # a static figure genuinely cannot do.
    hover_data={"hours": ":.1f", "score": ":.1f", "group": True},
    title="Study hours vs exam score (hover a point)",
    labels={"hours": "hours studied", "score": "exam score"},
)
figure.update_layout(template="plotly_white")
save_html(figure, __file__, "scatter")

# --- 2. zoom is the other reason -------------------------------------------
monthly = sales()
figure = px.line(
    monthly, x="month", y="sales", color="region",
    title="Sales by region (drag to zoom, double-click to reset)",
    template="plotly_white",
)
figure.update_traces(hovertemplate="%{y:.0f}k")
save_html(figure, __file__, "lines")

# --- 3. facets: small multiples, for free ----------------------------------
figure = px.line(
    monthly, x="month", y="sales", facet_col="region", facet_col_wrap=2,
    title="One panel per region, shared axes",
    template="plotly_white", height=520,
)
save_html(figure, __file__, "facets")

print("""
  plotly.express is the seaborn of interactive charts: one call, one chart.
  Reach for it when the reader needs to hover or zoom.
  In Streamlit:  st.plotly_chart(fig, use_container_width=True)
""")
