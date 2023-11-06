import streamlit as st
import pandas


st.subheader("***Session State***")
st.write('Session State is a way to share variables between reruns, for each user session. In addition to the ability to store and persist state, Streamlit also exposes the ability to manipulate state using Callbacks. Session state also persists across apps inside a multipage app.')

with st.echo():

    if 'key' not in st.session_state: # Initialization
        st.session_state['key'] = 'value'

    # Session State also supports attribute based syntax
    if 'key' not in st.session_state:
        st.session_state.key = 'value'

    # Read
    print(st.session_state.key)

    # Update an item in Session State by assigning it a value:
    st.session_state.key = 'value2'  # Attribute API
    st.session_state['key'] = 'value2'  # Dictionary like API

    # Delete a single key-value pair
    del st.session_state['key']
