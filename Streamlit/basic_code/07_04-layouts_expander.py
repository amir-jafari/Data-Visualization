import streamlit as st

st.subheader("***Expander***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

    with st.expander("See explanation"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)
        st.image("https://static.streamlit.io/examples/dice.jpg")
