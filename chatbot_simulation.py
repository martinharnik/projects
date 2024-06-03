import streamlit as st
import time

# Function to simulate typing effect
def type_message(role, message):
    typed_message = ""
    message_placeholder = st.empty()
    for char in message:
        typed_message += char
        message_placeholder.markdown(f"**{role}:** {typed_message}")
        time.sleep(0.04)  # Adjust the speed of typing here

# Define the conversation steps
conversation = [
    ("Shaun", "Hey L’Oréal GPT, quick question: what's 1+1?"),
    ("L’Oréal GPT", "Isn’t that the Czech Rossmann promotion you're always raving about?"),
    ("Shaun", "No, L’Oréal GPT, that's how CPD is projecting incremental growth in 2025. We're aiming to increase basket size with our new '+1 gesture' approach."),
    ("L’Oréal GPT", "'+1 gesture'? Tell me more about this intriguing strategy."),
    ("Shaun", "I thought I was supposed to be picking your digital brain! Okay, so the '+1 gesture' is all about encouraging consumers to adopt new beauty habits and extend their routine. And a big part of that is tapping into the massive potential of the men's segment."),
    ("L’Oréal GPT", "Excellent point, Shaun. We're seeing men become increasingly interested in skincare, haircare, and even makeup. The opportunities there are substantial."),
    ("Shaun", "Absolutely. In 2024, the key new beauty habits we're seeing emerge across the board are serums, specialized hair treatments, daily UV protection, primers, and blushes. The million-euro question is: how do we capitalize on this and really drive routine expansion across all consumer groups, especially men?"),
    ("L’Oréal GPT", "It's tricky. Consumers are bombarded with over 200 touchpoints daily. Cutting through that noise is paramount. For men, in particular, we need messaging and channels that resonate with their preferences. But luckily you have about 15 men in the business development department"),
    ("Shaun", "For sure. Some initial thoughts are targeted media campaigns and influencer advocacy. Then there's strategic sampling, creative promotions, optimizing the online and in-store shopper experience, and perhaps some event-based marketing tailored to a male audience."),
    ("L’Oréal GPT", "For in-store, I recommend exploring **TADA**, also known as **TAD-AI**, our supplemental AI package designed for point-of-sale engagement."),
    ("Shaun", "Interesting. I'll have to look into downloading **TADA AI**. This whole thing feels data-heavy. We'll need robust business intelligence to stay on top of it."),
    ("L’Oréal GPT", "You're speaking my language! Might I suggest **STANDA**, or **STAND-AI**? It's our flagship business intelligence software. Unparalleled data insights and reporting, particularly within the realm of '+1 gestures.'"),
    ("Shaun", "We’ll need to premiumize the business a bit in order to fund all these projects GPT!"),
    ("L’Oréal GPT", "Correct Shaun, and have you heard about Revenue Growth Management? With the additional excel add-in known as **VALORIZ-AI**, you’ll be premiumizing almost instantly"),
    ("Shaun", "This is going to be quite the strategic adventure, GPT."),
    ("L’Oréal GPT", "Indeed it will be. Now, are you going to actually present something or are we going to spend the rest of the day chatting?"),
    ("Shaun", "Right, let's do this!"),
]

# Add the title
st.title("Loreal GPT")

# Initial delay before starting the conversation
time.sleep(2)

# Display the conversation with delay and typing effect
for role, message in conversation:
    type_message(role, message)
    time.sleep(3)
