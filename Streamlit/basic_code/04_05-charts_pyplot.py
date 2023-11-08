import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Pyplot***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)

    st.pyplot(fig)
