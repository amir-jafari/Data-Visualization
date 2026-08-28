import streamlit as st

st.subheader("***Sidebar***")

code = """
# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
"""

st.code(code, language='python')
exec(code)

st.write("See the display result of the left sidebar")
