"""
Map dashboard -- four ways to put data on a map, and when to use each.

01_basics/03_charts/09_map.py shows st.map in one line. This is what you reach
for when one line is not enough: tooltips, sizing by a value, aggregating
thousands of points, and clickable popups.

What it shows:
    * st.map        -- one line, zero configuration
    * pydeck scatter-- size and colour carry a value, points have tooltips
    * pydeck hexagon-- points binned into 3D cells, for when there are too
                       many to read individually
    * folium        -- circles with clickable popups, rendered through
                       st.components.v1.html (streamlit-folium is not needed)

Data: a built-in table of 25 US cities, so this app needs no keys and no
network -- or upload any CSV that has latitude and longitude columns.

    streamlit run 02_apps/geospatial/map_dashboard/main.py
"""

import streamlit as st

import utils


def main():
    st.header("Map Dashboard")
    st.divider()
    st.subheader("Step 1: Load the data")

    data = utils.load_data()
    if data is None:
        st.stop()

    st.write(data.head())

    st.divider()
    st.subheader("Step 2: Say which columns are the coordinates")

    columns = list(data.columns)
    numeric = list(data.select_dtypes("number").columns)

    if len(numeric) < 2:
        st.error("A map needs at least two numeric columns (latitude and longitude).")
        st.stop()

    guess_lat = utils.guess_column(numeric, ["lat"])
    guess_lon = utils.guess_column(numeric, ["lon", "lng"])

    col1, col2, col3 = st.columns(3)
    with col1:
        lat = st.selectbox("Latitude", numeric,
                           index=numeric.index(guess_lat) if guess_lat in numeric else 0)
    with col2:
        lon = st.selectbox("Longitude", numeric,
                           index=numeric.index(guess_lon) if guess_lon in numeric else min(1, len(numeric) - 1))
    with col3:
        others = [c for c in numeric if c not in (lat, lon)]
        value = st.selectbox("Value to size/colour by", others) if others else None

    if lat == lon:
        st.error("Latitude and longitude must be different columns.")
        st.stop()

    # A point with a missing coordinate cannot be drawn, and some map layers
    # fail outright rather than skipping it.
    frame = data.dropna(subset=[lat, lon] + ([value] if value else []))

    off_globe = ((frame[lat].abs() > 90) | (frame[lon].abs() > 180)).sum()
    if off_globe:
        st.warning(f"{off_globe} row(s) have coordinates outside the valid range "
                   f"(latitude ±90, longitude ±180). They are probably not really "
                   f"coordinates -- check the two columns above.")
        frame = frame[(frame[lat].abs() <= 90) & (frame[lon].abs() <= 180)]

    if frame.empty:
        st.error("No rows left with usable coordinates.")
        st.stop()

    label_candidates = [c for c in columns if c not in numeric]
    label = st.selectbox("Label for tooltips (optional)", ["(none)"] + label_candidates)
    label = None if label == "(none)" else label

    st.divider()
    st.subheader("Step 3: Filter")

    if value:
        low, high = float(frame[value].min()), float(frame[value].max())
        if low < high:
            chosen = st.slider(f"Range of {value}", low, high, (low, high))
            frame = frame[frame[value].between(*chosen)]

    st.caption(f"{len(frame)} of {len(data)} rows on the map.")
    if frame.empty:
        st.warning("The filter removed everything. Widen the range.")
        st.stop()

    st.divider()
    st.subheader("Step 4: Four ways to draw it")

    tab1, tab2, tab3, tab4 = st.tabs(["st.map", "Scatter (pydeck)",
                                      "Hexagons (pydeck)", "Popups (folium)"])

    with tab1:
        st.write("***st.map*** -- built in, one line, no options worth speaking of. "
                 "Every point looks the same. Start here; move on when that stops "
                 "being enough.")
        utils.simple_map(frame, lat, lon)

    with tab2:
        if not value:
            st.info("This view sizes points by a value, and this data has no spare "
                    "numeric column to use.")
        else:
            st.write(f"***pydeck scatter*** -- radius carries **{value}**, and hovering "
                     f"a point shows its details. This is the workhorse view.")
            utils.scatter_map(frame, lat, lon, value, label)

    with tab3:
        if not value:
            st.info("This view needs a numeric column to set the bar heights.")
        else:
            st.write(f"***pydeck hexagons*** -- points are binned into cells and the "
                     f"height is the total **{value}** in each. Use this when you have "
                     f"thousands of points and individual dots are just a smear. Drag "
                     f"with the right mouse button to tilt the camera.")
            utils.hexagon_map(frame, lat, lon, value)

    with tab4:
        if not value:
            st.info("This view sizes circles by a value, and none is available.")
        else:
            st.write("***folium*** -- click any circle for a popup. Rendered straight "
                     "to HTML, so it needs no extra package beyond folium itself.")
            utils.folium_map(frame, lat, lon, value, label)


if __name__ == "__main__":
    main()
