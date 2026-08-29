import streamlit as st
import time

st.subheader("***Write stream***")
st.write(
    "`st.write_stream()` prints text **as it arrives**, word by word, instead of "
    "waiting for the whole answer. This is how a chatbot gets its typing effect -- "
    "the chat apps in `apps/nlp/chatbot/` use exactly this."
)

st.write("It takes a *generator*: a function that `yield`s pieces instead of `return`ing once.")


# st.echo(): use in a with block to draw some code on the app, then execute it.
with st.echo():
    def slow_reply():
        answer = "Hello there! I am pretending to think while I type this out."
        for word in answer.split():
            yield word + " "
            time.sleep(0.05)

    if st.button("Ask the bot"):
        # write_stream draws each piece as it is yielded, and returns the full text
        full_text = st.write_stream(slow_reply)
        st.write("---")
        st.write("The complete answer was:", full_text)

st.info(
    "A real LLM gives you a generator too, so you swap `slow_reply` for the "
    "model's stream and nothing else changes."
)
