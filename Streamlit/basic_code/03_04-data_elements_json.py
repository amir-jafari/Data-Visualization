import streamlit as st

# %%--------------------------------------------------------------------------------------------------------------------

st.subheader("***Dicts and JSON***")
st.write("Display object or string as a pretty-printed JSON string.")

code = """
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
"""

st.code(code, language='python')
exec(code)
