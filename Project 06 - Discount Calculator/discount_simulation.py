import streamlit as st
from datetime import datetime
import time
import random

# Custom CSS for gradient background, title position, hiding top margin, Arial font, and default select box option
st.markdown(
    """
    <style>
    @font-face {
        font-family: 'Arial';
        font-weight: normal;
        font-style: normal;
    }
    
    .stApp {
        background: linear-gradient(to bottom, #000028, #009999);
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .title {
        font-size: 32px;
        font-weight: bold;
        color: white;
    }
    .subtitle {
        font-size: 24px;
        color: white;
    }
    [data-testid="stDecoration"] {
        display: none;
    }
    .css-1awozwy option[value=""] {
        color: gray;
    }
    .stButton button {
        background-color: black; /* Set button background to black */
        color: #F5F5F5;
        border-radius: 4px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
        font-family: 'Arial', sans-serif;
        cursor: pointer;
    }
    .stButton button:hover {
        color: white; /* Change text color to white on hover */
        background-color: #333; /* Slightly lighter black for hover effect */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the Siemens logo
#st.image('sag-logo.png', width=175)

# Title of the application
st.markdown('<div class="title">Discount Calculator</div>', unsafe_allow_html=True)

# Display a message in the main area about the business value
st.markdown("""
Enter your parameters below and click on "Calculate Optimal Discount" to see the potential benefits for your business.

If you are not sure what to input, hover over the little help buttons next to each field to see an explanation.
""")

# Form for input parameters
with st.form(key='predict_form'):
    sales_district = st.selectbox("Sales District", options=[""] + ["Northern Europe", "Central America", "Southeast Asia", "Eastern Africa", "Western Australia"], index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Sales District from the list")
    customer_name = st.selectbox("Customer Name", options=[""] + ["GlobalTech Solutions", "Innovatech Industries", "GreenWave Enterprises", "NexaCorp International", "FutureLink Systems"], index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Customer Name from the list")
    product_category = st.selectbox("Product Category", options=[""] + ["Energy", "Healthcare", "Industrial Automation", "Mobility", "Digital Industries"], index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Product Category from the list")
    product_sub_category = st.selectbox("Product Sub-Category", options=[""] + ["Robotics", "Motion Control", "Industrial Ethernet"], index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Product Sub-Category from the list")
    item_name = st.selectbox("Item Name", options=[""] + ["Assembly Line", "Solar Power System", "Digital X-Ray Machine", "Electric Vehicle Charging Station"], index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Item Name from the list")
    item_count = st.number_input("Item Count", min_value=0, value=0, format='%d', step=1, key='item_count', help="Enter the total number of items in the order")
    
    # Calculate Optimal Discount button
    predict_button = st.form_submit_button(label='Calculate Optimal Discount')

# Mimic processing after hitting the button
if predict_button:
    with st.spinner('Calculating...'):
        time.sleep(2)  # Simulate a short processing time
    item_price = random.uniform(500, 10000)
    optimal_discount = random.uniform(30, 80)
    discounted_price = item_price * (1 - optimal_discount / 100)
    
    st.write(f"### Item Price (EUR): {item_price:.2f}")
    st.write(f"### Optimal Discount: {optimal_discount:.2f}%")
    st.write(f"### Discounted Price (EUR): {discounted_price:.2f}")
