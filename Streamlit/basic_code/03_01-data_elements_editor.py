import streamlit as st
import pandas as pd
from datetime import datetime, date, time

# %%--------------------------------------------------------------------------------------------------------------------
st.subheader("***Data editor***")
st.write("Use to display and interact with raw data. Edit dataframes and many other data structures in a table-like UI.")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    df = pd.DataFrame(
        [
           {"command": "st.selectbox", "rating": 4, "is_widget": True},
           {"command": "st.balloons", "rating": 5, "is_widget": False},
           {"command": "st.time_input", "rating": 3, "is_widget": True},
       ]
    )

    # allow the user to add and delete rows by setting num_rows to "dynamic"
    edited_df = st.data_editor(df, num_rows="dynamic")

    favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
    st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
