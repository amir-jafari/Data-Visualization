import streamlit as st
import pandas


st.subheader("***Help***")
st.write('Display help and other information for a given object.')

with st.echo():
    st.help(pandas.DataFrame)
