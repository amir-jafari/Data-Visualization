import streamlit as st
import numpy as np
import pandas as pd

# --- make Streamlit/s3_utils.py importable from any sub-folder ----------------
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents
                            if (p / "s3_utils.py").is_file())))
import s3_utils

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Download button***")

st.write("***Download an image***")
st.write("The image is fetched from S3 first, then handed to the download button.")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    # s3://dats-dl/ajafari@gwu.edu/streamlit/static/flower.png
    # read_bytes() stops the app with a "keys need updating" message if S3 refuses us.
    data = s3_utils.read_bytes('static/flower.png')

    btn = st.download_button(
            label="Download image",
            data=data,
            file_name="flower.png",
            mime="image/png"
          )

st.caption(f"Source: {s3_utils.uri('static/flower.png')}")


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
