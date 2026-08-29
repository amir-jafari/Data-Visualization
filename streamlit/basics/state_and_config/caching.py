import streamlit as st
import time

st.subheader("***Caching***")
st.write(
    "Streamlit re-runs your whole script on every interaction, so a slow step "
    "would run again every single time. A cache decorator tells Streamlit: "
    "*you already did this, reuse the answer.*"
)

st.divider()
st.write("***@st.cache_data -- for data (a DataFrame, a list, a number)***")
st.write("Streamlit stores a **copy** of the return value, keyed by the arguments.")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    @st.cache_data
    def slow_square(n):
        time.sleep(2)          # pretend this is a big download or query
        return n * n

    number = st.slider("Pick a number", 1, 10, 3)

    start = time.time()
    answer = slow_square(number)
    elapsed = time.time() - start

    st.write(f"{number} squared is {answer} -- took {elapsed:.2f} seconds")

st.info(
    "Move the slider to a **new** number: it takes 2 seconds. Move it **back** "
    "to a number you already picked: it is instant. That is the cache."
)

st.divider()
st.write("***@st.cache_resource -- for things you cannot copy (a model, a connection)***")
st.write(
    "Same idea, but every user shares the **same object** instead of a copy. "
    "This is what you use to load an ML model once instead of on every click."
)

with st.echo():
    @st.cache_resource
    def load_model():
        time.sleep(2)          # pretend this is model.from_pretrained(...)
        return {"name": "my-pretend-model"}

    model = load_model()
    st.write("Model is ready:", model["name"])

st.success("Reload this page -- the model is not loaded a second time.")

st.divider()
st.write("***Which one do I use?***")
st.write(
    "- `@st.cache_data` -> the function returns **data**: a DataFrame, a dict, a number.\n"
    "- `@st.cache_resource` -> the function returns a **thing you reuse**: an ML model, "
    "a database connection.\n\n"
    "Use `st.cache_data.clear()` or `st.cache_resource.clear()` to empty them by hand."
)
