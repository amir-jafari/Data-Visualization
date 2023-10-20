import streamlit as st
import numpy as np
import time

# %%--------------------------------------------------------------------------------------------------------------------
st.header("Layouts and Containers")
st.write("Streamlit provides several options for controlling how different elements are laid out on the screen.")


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
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


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Columns***")

code = """
col1, col2, col3 = st.columns(3)

with col1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg")
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Tabs***")

code = """
tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
data = np.random.randn(10, 1)

tab1.subheader("A tab with a chart")
tab1.line_chart(data)

tab2.subheader("A tab with the data")
tab2.write(data)
"""

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Expander***")

code = """
st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.expander("See explanation"):
    st.write(\"\"\"
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    \"\"\")
    st.image("https://static.streamlit.io/examples/dice.jpg")
"""

st.code(code, language='python')
exec(code)

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Container***")
st.write("Insert a multi-element container.")
st.write("Inserts an invisible container into your app that can be used to hold multiple elements. This allows you to, for example, insert multiple elements into your app out of order.")

code = """
with st.container():
   st.write("This is inside the container")

   # You can call any Streamlit command, including custom components:
   st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container")
"""

st.code(code, language='python')
exec(code)


# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.subheader("***Empty***")
st.write("Insert a single-element container.")
st.write("Inserts a container into your app that can be used to hold a single element. This allows you to, for example, remove elements at any point, or replace several elements at once (using a child multi-element container).")

st.write('***Overwriting elements in-place using "with" notation:***')

code = """
with st.empty():
    for seconds in range(60):
        st.write(f"⏳ {seconds} seconds have passed")
        time.sleep(1)
    st.write("✔️ 1 minute over!")
"""

st.code(code, language='python')
exec(code)