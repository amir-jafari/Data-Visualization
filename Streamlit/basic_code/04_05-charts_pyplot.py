import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Pyplot***")

code = """
arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)
"""

st.code(code, language='python')
exec(code)
