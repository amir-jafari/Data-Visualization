import streamlit as st
import time

st.subheader("***Fragment***")
st.write(
    "A function decorated with `@st.fragment` re-runs **on its own** when you "
    "touch a widget inside it -- the rest of the page is left alone. That keeps a "
    "small interactive corner fast even when the page around it is slow."
)

st.write("This timestamp is from the **whole page**:", time.strftime("%H:%M:%S"))


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    @st.fragment
    def just_this_bit():
        st.slider("Move me", 0, 100, 50)
        st.write("Fragment last ran at:", time.strftime("%H:%M:%S"))

    just_this_bit()

st.info(
    "Move the slider: only the fragment's time changes. Press the button below: "
    "the whole page re-runs and **both** times change."
)
st.button("Re-run the whole page")
