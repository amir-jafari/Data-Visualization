import streamlit as st

st.subheader("***Session State***")
st.write(
    "Streamlit re-runs the whole script on every interaction, so a normal "
    "variable is created from scratch each time. `st.session_state` is a "
    "dictionary that **survives** those re-runs, for this browser tab."
)

st.divider()
st.write("***First, the problem***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    plain_counter = 0
    if st.button("Add one to the plain variable"):
        plain_counter += 1
    st.write("Plain variable:", plain_counter)   # always 0 or 1 -- never 2

st.warning("It never gets past 1: the script starts over and `plain_counter = 0` runs again.")

st.divider()
st.write("***Now with session state***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    # Initialise once -- the `if` is what stops it resetting on every re-run.
    if "count" not in st.session_state:
        st.session_state.count = 0

    if st.button("Add one to session state"):
        st.session_state.count += 1

    st.write("Session state:", st.session_state.count)   # keeps climbing

st.success("This one keeps counting, because the value is stored between re-runs.")

st.divider()
st.write("***The syntax***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    st.session_state.my_key = "hello"       # attribute style
    st.session_state["my_key"] = "hello"    # dictionary style -- same thing

    st.write(st.session_state.my_key)       # read
    st.write("Is 'my_key' set?", "my_key" in st.session_state)

    del st.session_state["my_key"]          # delete
