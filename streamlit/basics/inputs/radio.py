import streamlit as st

st.subheader("***Radio***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    genre = st.radio(
        "What's your favorite movie genre",
        [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
        captions = ["Laugh out loud.", "Get the popcorn.", "Never stop learning."],
        index=None,
    )

    st.write("You selected:", genre)

