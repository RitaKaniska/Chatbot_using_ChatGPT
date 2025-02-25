import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load API Key from Streamlit secrets (Replace with a proper method)
openai.api_key = st.secrets["openai"]["api_key"]

st.title("Simple Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What can I help you with today?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # Store user input
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response using OpenAI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True,
            )

            for chunk in response:
                delta_content = chunk["choices"][0]["delta"].get("content", "")
                full_response += delta_content
                message_placeholder.markdown(full_response + " ▌")

            message_placeholder.markdown(full_response)

            # Store assistant's response
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error: {e}")
