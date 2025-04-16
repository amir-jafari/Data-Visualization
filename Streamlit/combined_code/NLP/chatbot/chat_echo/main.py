# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import streamlit as st

st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input

# We used the := operator to assign the user's input to the prompt variable and checked if it's not None in the same line. If the user has sent a message, we display the message in the chat message container and append it to the chat history.

# The := operator, introduced in Python 3.8, is known as the "walrus operator." It is an assignment expression operator, which means that it assigns a value to a variable as part of an expression and returns the assigned value.

if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
