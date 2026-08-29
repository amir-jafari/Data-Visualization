import streamlit as st

st.subheader("***Rerun***")
st.write(
    "`st.rerun()` restarts the script immediately, from line 1. You need it when "
    "you change something that the page has *already drawn* and you want the page "
    "to reflect it right away."
)


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    if "count" not in st.session_state:
        st.session_state.count = 0

    st.write("Count is:", st.session_state.count)

    if st.button("Add one, then rerun"):
        st.session_state.count += 1
        st.rerun()          # start over -- the line above now prints the new value

st.divider()
st.warning(
    "Careful: `st.rerun()` inside a plain `if` with no condition to stop it is an "
    "infinite loop. Always change some state first, so the next run takes a "
    "different path."
)
