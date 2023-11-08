import streamlit as st

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Button***")

st.write("***Regular Button***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    st.button("Reset", type="primary")
    if st.button('Say hello'):
        st.write('Why hello there')
    else:
        st.write('Goodbye')


st.write("##")
st.write("***Link button***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    st.link_button("Go to gallery", "https://streamlit.io/gallery")
