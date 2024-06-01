import streamlit as st
import time

# Function to simulate typing effect
def type_message(role, message):
    typed_message = ""
    message_placeholder = st.empty()
    for char in message:
        typed_message += char
        message_placeholder.markdown(f"**{role}:** {typed_message}")
        time.sleep(0.05)  # Adjust the speed of typing here

# Define the conversation steps
conversation = [
    ("Shaun", "Hey LOréal GPT, quick question: what's 1+1?"),
    ("LOréal GPT", "Isn’t that the Czech Rossmann promotion you're always raving about?"),
    ("Shaun", "No, LOréal GPT, that's how CPD is projecting incremental growth in 2025. We're aiming to increase basket size with our new '+1 gesture' approach."),
    ("LOréal GPT", "'+1 gesture'? Tell me more about this intriguing strategy."),
]

# Add the title
st.title("Loreal GPT")

# Display the conversation with delay and typing effect
for role, message in conversation:
    type_message(role, message)
    time.sleep(3)
