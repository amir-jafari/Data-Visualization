import streamlit as st
import time

st.subheader("***Empty***")
st.write("Insert a single-element container.")
st.write("Inserts a container into your app that can be used to hold a single element. This allows you to, for example, remove elements at any point, or replace several elements at once (using a child multi-element container).")

st.write('***Overwriting elements in-place using "with" notation:***')


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    with st.empty():
        for seconds in range(60):
            st.write(f"⏳ {seconds} seconds have passed")
            time.sleep(1)
        st.write("✔️ 1 minute over!")
