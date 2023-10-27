import streamlit as st
import numpy as np
import pandas as pd

st.subheader("***Display Highlighted DataFrame***")
st.write("st.dataframe() can also be helpful to render dataframe in different styles")
code = """df = pd.DataFrame(
   np.random.randn(5, 10),
   columns=('col %d' % i for i in range(00)))

st.dataframe(df.style.highlight_max(axis=0))
"""

st.code(code, language='python')

df = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(5, 10)),
    columns=('col %d' % i for i in range(10)))

st.dataframe(df.style.highlight_max(axis=0))

st.write("In this example we highlight the highest value in each column")
st.write("We can also customize the dataframe to show plots in the cells")
