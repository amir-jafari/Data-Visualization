import streamlit as st
import datetime

st.subheader("***Date-time input***")

code = '''
d = st.date_input("When's your birthday", value=None)
st.write('Your birthday is:', d)

today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

d = st.date_input(
    "Select your vacation for next year",
    (jan_1, datetime.date(next_year, 1, 7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)
d

t = st.time_input('Set an alarm for', datetime.time(8, 45))
st.write('Alarm is set for', t)
'''

st.code(code, language='python')
exec(code)

