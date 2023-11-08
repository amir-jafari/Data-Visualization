import streamlit as st
import numpy as np
import pandas as pd

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Display DataFrame***")
st.write("This variable can be any data format.")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    df = pd.DataFrame(
        np.random.randint(low=0, high=100, size=(5, 10)),
        columns=('col %d' % i for i in range(10))
    )

    st.dataframe(df)
