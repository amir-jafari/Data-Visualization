import streamlit as st
import os
import numpy as np
import pandas as pd

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Download button***")

st.write("***Download an image***")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('..')

    path = os.getcwd() + os.path.sep + 'static' + os.path.sep + 'flower.png'

    with open(path, "rb") as file:
        btn = st.download_button(
                label="Download image",
                data=file,
                file_name="flower.png",
                mime="image/png"
              )


st.write('#')
st.write("***Download a large DataFrame as a CSV***")

code = '''
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

my_large_df = pd.DataFrame(
   {
       "col1": list(range(20)) * 3,
       "col2": np.random.randn(60),
       "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,
   }
)

csv = convert_df(my_large_df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)
'''

st.code(code, language='python')
exec(code)
