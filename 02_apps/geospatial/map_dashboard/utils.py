"""Sample data, column detection and the four map renderers."""

import folium
import pandas as pd
import pydeck as pdk
import streamlit as st
import streamlit.components.v1 as components

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils

# 25 US cities: name, latitude, longitude, population (2020 census, thousands).
# Hard-coded on purpose -- this app works with no S3 keys and no network data,
# so it is the one you can always fall back on.
SAMPLE = pd.DataFrame(
    [("New York", 40.7128, -74.0060, 8804),
     ("Los Angeles", 34.0522, -118.2437, 3899),
     ("Chicago", 41.8781, -87.6298, 2746),
     ("Houston", 29.7604, -95.3698, 2304),
     ("Phoenix", 33.4484, -112.0740, 1608),
     ("Philadelphia", 39.9526, -75.1652, 1603),
     ("San Antonio", 29.4241, -98.4936, 1434),
     ("San Diego", 32.7157, -117.1611, 1386),
     ("Dallas", 32.7767, -96.7970, 1304),
     ("San Jose", 37.3382, -121.8863, 1013),
     ("Austin", 30.2672, -97.7431, 961),
     ("Jacksonville", 30.3322, -81.6557, 949),
     ("Fort Worth", 32.7555, -97.3308, 918),
     ("Columbus", 39.9612, -82.9988, 905),
     ("Charlotte", 35.2271, -80.8431, 874),
     ("Indianapolis", 39.7684, -86.1581, 887),
     ("San Francisco", 37.7749, -122.4194, 873),
     ("Seattle", 47.6062, -122.3321, 737),
     ("Denver", 39.7392, -104.9903, 715),
     ("Washington", 38.9072, -77.0369, 689),
     ("Boston", 42.3601, -71.0589, 675),
     ("Nashville", 36.1627, -86.7816, 689),
     ("Detroit", 42.3314, -83.0458, 639),
     ("Portland", 45.5152, -122.6784, 652),
     ("Las Vegas", 36.1699, -115.1398, 641)],
    columns=["city", "lat", "lon", "population"])


def guess_column(columns, wanted):
    """Find the column whose name looks like a latitude/longitude/value column."""
    for candidate in wanted:
        for column in columns:
            if candidate in str(column).lower():
                return column
    return None


def load_data():
    """The built-in sample, or a CSV of your own."""
    source = st.radio("Data", ["Sample: 25 US cities", "Upload my own CSV"],
                      horizontal=True)

    if source.startswith("Sample"):
        st.caption("No keys and no network needed -- this table is built into the app.")
        return SAMPLE.copy()

    upload = st.file_uploader("A CSV with latitude and longitude columns", type=["csv"])
    if upload is None:
        st.info("Waiting for a CSV. It needs one column of latitudes and one of "
                "longitudes; anything else becomes the value you colour and size by.")
        return None

    return pd.read_csv(upload)


def view_state(frame, lat, lon):
    """Centre the map on the data rather than on a hard-coded place."""
    return pdk.ViewState(latitude=float(frame[lat].mean()),
                         longitude=float(frame[lon].mean()),
                         zoom=3, pitch=0)


def simple_map(frame, lat, lon):
    """st.map -- one line, no configuration, good enough surprisingly often."""
    st.map(frame.rename(columns={lat: "latitude", lon: "longitude"}),
           latitude="latitude", longitude="longitude")


def scatter_map(frame, lat, lon, value, label):
    """pydeck scatter: radius carries the value, and points get a tooltip."""
    biggest = max(frame[value].max(), 1)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=frame,
        get_position=[lon, lat],
        get_radius=f"{value} / {biggest} * 60000 + 8000",
        get_fill_color=[220, 60, 60, 160],
        pickable=True,
    )

    tooltip = {"text": f"{{{label}}}\n{value}: {{{value}}}"} if label else {"text": f"{value}: {{{value}}}"}
    st.pydeck_chart(pdk.Deck(layers=[layer],
                             initial_view_state=view_state(frame, lat, lon),
                             map_provider="carto", map_style="light",
                             tooltip=tooltip))


def hexagon_map(frame, lat, lon, value):
    """pydeck hexagons: points aggregated into 3D bins, height = total value.

    Useful when you have far too many points to read individually.
    """
    layer = pdk.Layer(
        "HexagonLayer",
        data=frame,
        get_position=[lon, lat],
        get_elevation_weight=value,
        elevation_scale=50,
        radius=50000,
        extruded=True,
        pickable=True,
    )
    st.pydeck_chart(pdk.Deck(layers=[layer],
                             initial_view_state=pdk.ViewState(
                                 latitude=float(frame[lat].mean()),
                                 longitude=float(frame[lon].mean()),
                                 zoom=3, pitch=40),
                             map_provider="carto", map_style="light"))


def folium_map(frame, lat, lon, value, label, height=520):
    """folium: circles sized by value, each with a clickable popup.

    streamlit-folium is not installed on the course server, so the map is
    rendered to HTML and dropped into the page as a component -- plain folium,
    no extra dependency.
    """
    centre = [float(frame[lat].mean()), float(frame[lon].mean())]
    fmap = folium.Map(location=centre, zoom_start=4, tiles="cartodbpositron")

    biggest = max(frame[value].max(), 1)
    for _, row in frame.iterrows():
        name = row[label] if label else ""
        folium.CircleMarker(
            location=[row[lat], row[lon]],
            radius=4 + 20 * (row[value] / biggest),
            popup=folium.Popup(f"<b>{name}</b><br>{value}: {row[value]:,}", max_width=200),
            tooltip=str(name) or None,
            color="#c0392b", fill=True, fill_opacity=0.5, weight=1,
        ).add_to(fmap)

    components.html(fmap.get_root().render(), height=height)
