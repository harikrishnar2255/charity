import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Groq Chatbot", page_icon="💬", layout="centered")

st.title("💬 Groq Chatbot")
st.caption("Powered by Groq and openai/gpt-oss-120b")

# 2. Load environment variables from the .env file
load_dotenv()

# 3. Retrieve the API key from .env using the key name 'x'
api_key = os.getenv("x")

if not api_key:
    st.error("Groq API key under name 'x' was not found in your .env file.")
    st.stop()

# 4. Initialize the Groq client
client = Groq(api_key=api_key)
MODEL_ID = "openai/gpt-oss-120b"

# 5. Initialize Streamlit session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful and concise AI assistant."}
    ]

# Display prior chat messages (excluding the system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Accept user input from the chat bar
if user_input := st.chat_input("Type your message here..."):
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response using streaming
    with st.chat_message("assistant"):
        try:
            response_stream = client.chat.completions.create(
                model=MODEL_ID,
                messages=st.session_state.messages,
                stream=True
            )

            # Stream response chunk by chunk onto the UI
            full_response = st.write_stream(
                chunk.choices[0].delta.content or "" 
                for chunk in response_stream 
                if chunk.choices[0].delta.content
            )

            # Save assistant response to session history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"An error occurred: {e}")