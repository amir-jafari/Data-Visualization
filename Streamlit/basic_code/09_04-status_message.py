import streamlit as st

st.subheader("***Message***")
st.write("Display status messages.")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    st.error('This is an error', icon="🚨")

    st.warning('This is a warning', icon="⚠️")

    st.info('This is a purely informational message', icon="ℹ️")

    st.success('This is a success message!', icon="✅")

    e = RuntimeError('This is an exception of type RuntimeError')
    st.exception(e)
