"""
Altair -- charts as a grammar, and linked selections.

Altair makes you name the ENCODING: which column maps to x, to colour, to size,
and what kind of data each one is (quantitative, ordinal, nominal, temporal).
That is more typing than plotly for a quick chart, and it pays off the moment
you want two charts to talk to each other.

What it shows:
    * the encoding grammar, with the :Q / :N / :T type suffixes
    * why declaring the type matters -- get it wrong and the axis is wrong
    * a linked selection: brush one chart, filter the other

Run it:
    python viz/basics/interactive/altair_basics.py
    then open the .html files it prints
"""

import sys
from pathlib import Path

import altair as alt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save_html, sales, students        # noqa: E402

data = students()

# --- 1. the grammar --------------------------------------------------------
# x, y, colour are ENCODINGS; :Q means quantitative, :N nominal (unordered).
chart = (
    alt.Chart(data)
    .mark_circle(size=60, opacity=0.6)
    .encode(
        x=alt.X("hours:Q", title="hours studied"),
        y=alt.Y("score:Q", title="exam score"),
        color=alt.Color("group:N", title="group"),
        tooltip=["hours:Q", "score:Q", "group:N"],
    )
    .properties(width=520, height=340, title="Encoding: x, y, colour, tooltip")
)
save_html(chart, __file__, "encoding")

# --- 2. the type suffix is not decoration ----------------------------------
monthly = sales()

# :T tells Altair "this is time", so it gets a proper date axis.
correct = (
    alt.Chart(monthly).mark_line()
    .encode(x=alt.X("month:T", title="month"), y="sales:Q", color="region:N")
    .properties(width=520, height=260, title="month:T -- a real time axis")
)

# :N treats each date as an unrelated label: 24 categories, no ordering,
# equal spacing whatever the gaps.
wrong = (
    alt.Chart(monthly).mark_line()
    .encode(x=alt.X("month:N", title="month"), y="sales:Q", color="region:N")
    .properties(width=520, height=260, title="month:N -- 24 unrelated labels")
)
save_html(alt.vconcat(correct, wrong), __file__, "types")

# --- 3. linked selection: the thing altair is genuinely best at ------------
brush = alt.selection_interval(encodings=["x"])

upper = (
    alt.Chart(monthly).mark_line()
    .encode(x="month:T", y="sales:Q", color="region:N")
    .properties(width=520, height=200, title="Drag across this chart...")
    .add_params(brush)
)

lower = (
    alt.Chart(monthly).mark_bar()
    .encode(x="sum(sales):Q", y=alt.Y("region:N", sort="-x"), color="region:N")
    .properties(width=520, height=160, title="...and this one follows")
    .transform_filter(brush)
)

save_html(alt.vconcat(upper, lower), __file__, "linked-selection")

print("""
  Altair makes you say what each column IS:
    :Q quantitative   :N nominal   :O ordinal   :T temporal
  Get :T wrong and your dates become 24 unrelated categories.
  Its real strength is linked views -- brush one chart, filter another.
  In Streamlit:  st.altair_chart(chart, use_container_width=True)
""")
