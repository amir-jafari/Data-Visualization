import streamlit as st

# %%--------------------------------------------------------------------------------------------------------------------

st.subheader("***Dicts and JSON***")
st.write("Display object or string as a pretty-printed JSON string.")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    st.json({
        'foo': 'bar',
        'baz': 'boz',
        'stuff': [
            'stuff 1',
            'stuff 2',
            'stuff 3',
            'stuff 5',
        ],
    })
