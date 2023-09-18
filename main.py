import sys

import streamlit as st

from supabase_wrapper import log_message
from vectorstore import query_engine

st.set_page_config(
    page_title="Baldur's Gate 3 AI Guide", page_icon="🧙‍♀️")

st.image("./assets/splash.jpg", width=700)

st.title("Baldur's Gate 3 AI Guide")
            
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "What's on your mind?"}
    ]


# chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    log_message("user", prompt)
    

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_engine.query(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
            log_message("AI", response.response)