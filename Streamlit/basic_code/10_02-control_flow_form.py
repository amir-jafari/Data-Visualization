import streamlit as st

st.subheader("***Form***")
st.write('Create a form that batches elements together with a "Submit" button.')

code = """
with st.form("my_form"):
   st.write("Inside the form")
   slider_val = st.slider("Form slider")
   checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")
"""

st.code(code, language='python')

exec(code)
