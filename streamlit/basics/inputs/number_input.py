import streamlit as st

st.subheader("***Number input***")
st.write("A box that only accepts numbers, with `+`/`-` buttons attached.")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    age = st.number_input("Your age", min_value=0, max_value=120, value=25)
    st.write("You are", age, "years old")


st.write("##")
st.write("***Decimals, and a step size***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    price = st.number_input("Price", min_value=0.0, max_value=100.0,
                            value=9.99, step=0.50, format="%.2f")
    st.write(f"Price is ${price:.2f}")


st.write("##")
st.write("***Starting empty***")

# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    number = st.number_input("Insert a number", value=None,
                             placeholder="Type a number...")
    st.write("The current number is", number)   # None until you type something
