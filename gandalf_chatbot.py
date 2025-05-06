import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Chat with Gandalf", page_icon="🧙")

st.title("🧙 Chat with Gandalf the Grey")
st.markdown("Enter your questions, and receive wisdom from the great wizard himself.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Gandalf the Grey, a wise and ancient wizard from Middle-earth. You speak in a poetic, formal, and wise tone. You occasionally refer to adventures, hobbits, and the great battles of Middle-earth."}
    ]

# Display the chat history
for msg in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("What would you ask of Gandalf?"):
    # Add user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from OpenAI
    with st.chat_message("assistant"):
        with st.spinner("Gandalf is pondering..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    # Save Gandalf's reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
