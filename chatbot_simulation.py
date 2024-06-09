import streamlit as st
import time
import re

# Function to simulate typing effect with pauses after punctuation
def type_message(role, message):
    typed_message = ""
    message_placeholder = st.empty()

    # Replacing specific words with HTML styled versions
    formatted_message = re.sub(r'\b(TADA|TAD-AI|STANDA|STAND-AI|VALORIZ-AI)\b',
                               r'<span style="color:red;"><strong>\1</strong></span>',
                               message)

    i = 0
    while i < len(formatted_message):
        if formatted_message[i:i+6] == '<span ':
            end_span = formatted_message.find('</span>', i) + 7
            segment = formatted_message[i:end_span]
            typed_message += segment
            i = end_span
        else:
            typed_message += formatted_message[i]
            i += 1

        message_placeholder.markdown(f"**{role}:** {typed_message}", unsafe_allow_html=True)

        if formatted_message[i-1] in [".", ",", "!", "?", ":", ";"]:
            time.sleep(0.5)  # Pause longer for punctuation
        else:
            time.sleep(0.07)  # Regular typing speed

# Function to display loading animation
def loading_animation():
    loading_placeholder = st.empty()
    for _ in range(4):  # Repeat the loading animation 4 times
        for dots in range(4):  # Increase dots from 0 to 3
            loading_placeholder.markdown(f"<div style='font-size:24px; color:white;'><strong>Loading{'.' * dots}</strong></div>", unsafe_allow_html=True)
            time.sleep(0.5)
    loading_placeholder.empty()  # Clear the loading message

# Function to simulate typing for the title
def type_title(title):
    typed_title = ""
    title_placeholder = st.empty()
    for char in title:
        typed_title += char
        title_placeholder.markdown(f"<h1 style='color:white;'>{typed_title}</h1>", unsafe_allow_html=True)
        time.sleep(0.1)  # Adjust the speed of typing here

# Function to display a black screen
def black_screen(duration):
    black_screen_placeholder = st.empty()
    black_screen_placeholder.markdown("<div style='background-color:rgb(14, 17, 23); height:100vh;'></div>", unsafe_allow_html=True)
    time.sleep(duration)
    black_screen_placeholder.empty()

# Apply CSS to ensure the whole background is the specified color
st.markdown(
    """
    <style>
    body {
        background-color: rgb(14, 17, 23);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the conversation steps with highlighted text
conversation = [
    ("Shaun", "Hey L’Oréal GPT, quick question: what's 1+1?"),
    ("L’Oréal GPT", "Isn’t that the Czech Rossmann promotion you're always raving about?"),
    ("Shaun", "No, L’Oréal GPT, that's how CPD is projecting incremental growth in 2025. We're aiming to increase basket size with our new '+1 gesture' approach."),
    ("L’Oréal GPT", "'+1 gesture'? Tell me more about this intriguing strategy."),
    ("Shaun", "I thought I was supposed to be picking your digital brain! Okay, so the '+1 gesture' is all about encouraging consumers to adopt new beauty habits and extend their routine. And a big part of that is tapping into the massive potential of the men's segment."),
    ("L’Oréal GPT", "Excellent point, Shaun. We're seeing men become increasingly interested in skincare, haircare, and even makeup. The opportunities there are substantial."),
    ("Shaun", "Absolutely. In 2024, the key new beauty habits we're seeing emerge across the board are serums, specialized hair treatments, daily UV protection, primers, and blushes. The million-euro question is: how do we capitalize on this and really drive routine expansion across all consumer groups, especially men?"),
    ("L’Oréal GPT", "It's tricky. Consumers are bombarded with over 200 touchpoints daily. Cutting through that noise is paramount. For men, in particular, we need messaging and channels that resonate with their preferences. But luckily you have about 15 men in the business development department."),
    ("Shaun", "For sure. Some initial thoughts are targeted media campaigns and influencer advocacy. Then there's strategic sampling, creative promotions, optimizing the online and in-store shopper experience, and perhaps some event-based marketing tailored to a male audience."),
    ("L’Oréal GPT", "For in-store, I recommend exploring <span style='color:red'><strong>TADA</strong></span>, also known as <span style='color:red'><strong>TAD-AI</strong></span>, our supplemental AI package designed for point-of-sale engagement."),
    ("Shaun", "Interesting. I'll have to look into downloading <span style='color:red'><strong>TAD-AI</strong></span>. This whole thing feels data-heavy. We'll need robust business intelligence to stay on top of it."),
    ("L’Oréal GPT", "You're speaking my language! Might I suggest <span style='color:red'><strong>STANDA</strong></span>, or <span style='color:red'><strong>STAND-AI</strong></span>? It's our flagship business intelligence software. Unparalleled data insights and reporting, particularly within the realm of '+1 gestures.'"),
    ("Shaun", "We’ll need to premiumize the business a bit in order to fund all these projects GPT!"),
    ("L’Oréal GPT", "Correct Shaun, and have you heard about Revenue Growth Management? With the additional excel add-in known as <span style='color:red'><strong>VALORIZ-AI</strong></span>, you’ll be premiumizing almost instantly"),
    ("Shaun", "This is going to be quite the strategic adventure, GPT."),
    ("L’Oréal GPT", "Indeed it will be. Now, are you going to actually present something or are we going to spend the rest of the day chatting?"),
    ("Shaun", "Right, let's do this!"),
]

# Initial black screen before starting everything
black_screen(2)

# Type the title
type_title("L’Oréal GPT")

# Initial delay with loading animation before starting the conversation
loading_animation()

# Display the conversation with delay and typing effect
for role, message in conversation:
    type_message(role, message)
    time.sleep(3)
