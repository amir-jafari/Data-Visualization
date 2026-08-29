import streamlit as st

st.subheader("***Dialog***")
st.write(
    "A modal window that blocks the rest of the page until you deal with it. "
    "Use it for a confirmation, or a small form you do not want inline."
)


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    @st.dialog("Are you sure?")
    def confirm_delete():
        st.write("This would delete your data. (It will not -- this is a demo.)")
        name = st.text_input("Type your name to confirm")

        if st.button("Yes, delete it"):
            st.session_state.deleted_by = name
            st.rerun()          # closes the dialog and re-runs the page

    if st.button("Delete everything", type="primary"):
        confirm_delete()

    if "deleted_by" in st.session_state:
        st.success(f"Confirmed by: {st.session_state.deleted_by}")

st.info("Only one dialog can be open at a time, and `st.rerun()` is what closes it.")
