import streamlit as st
from datetime import datetime
import time

# Custom CSS for gradient background, title position, hiding top margin, Siemens Sans font, and default select box option
st.markdown(
    """
    <style>
    @font-face {
        font-family: 'SiemensSans';
        src: url('https://your-font-source/SiemensSans-Regular.woff2') format('woff2'),
             url('https://your-font-source/SiemensSans-Regular.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }
    
    .stApp {
        background: linear-gradient(to bottom, #000028, #009999);
        color: white;
        font-family: 'SiemensSans', sans-serif;
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
        background-color: rgb(14, 17, 23);
        color: white;
        border-radius: 4px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
        font-family: 'SiemensSans', sans-serif;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: rgb(14, 17, 23);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the application
st.markdown('<div class="title">SIEMENS</div>', unsafe_allow_html=True)
st.markdown('## Predictive Pricing Framework')

# Display a message in the main area about the business value
st.markdown("""
Enter your parameters below and click on "Calculate Optimal Discount" to see the potential benefits for your business.

If you are not sure what to input, hover over the little help buttons next to each field to see an explanation.
""")

# Form for input parameters
with st.form(key='predict_form'):
    created_order_header = st.date_input("Created Order Header", value=datetime.now(), help="Select the date when the order was created")
    sales_region_id = st.selectbox("Sales Region ID", options=[""] + sorted([10, 20, 21, 23, 24, 26, 27, 28, 29]), index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Sales Region ID from the list")
    sales_district_id = st.selectbox("Sales District ID", options=[""] + sorted([520, 1150, 5651, 5563, 301, 20, 230]), index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Sales District ID from the list")
    customer_branch = st.selectbox("Customer Branch", options=[""] + sorted(["Antarctica", "Asia", "Australia", "Europe", "North America", "South America"]), index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Customer Branch from the list")
    customer_importance = st.selectbox("Customer Importance", options=[""] + sorted(["Nezatříděno", "A Customer", "B Customer", "C Customer w. Potential", "C Customer w/o Potential", "T Customer", "V Customer"]), index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Customer Importance category")
    customer_bisnode_score = st.number_input("Customer Bisnode Score", min_value=0, value=0, format='%d', step=1, key='bisnode', help="Enter the credit risk score ranging from 1 (lowest risk) to 15 (highest risk)")
    item_count = st.number_input("Item Count", min_value=0, value=0, format='%d', step=1, key='item_count', help="Enter the total number of items in the order")
    item_price = st.number_input("Item Price (EUR)", min_value=0.0, value=0.0, step=0.01, format='%.2f', key='item_price', help="Enter the price per item in EUR")
    item_charge = st.number_input("Item Charge (EUR)", min_value=0.0, value=0.0, step=0.01, format='%.2f', key='item_charge', help="Enter the total charge for the items in EUR")
    product_category = st.selectbox("Product Category", options=[""] + sorted(["Energy", "Healthcare", "Industrial Automation", "Mobility", "Digital Industries"]), index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Product Category from the list")
    product_sub_category = st.selectbox("Product Sub-Category", options=[""] + sorted(["Robotics", "Motion Control", "Industrial Ethernet"]), index=0, format_func=lambda x: 'Choose an option' if x == "" else x, help="Select the Product Sub-Category from the list")
    
    # Calculate Optimal Discount button
    predict_button = st.form_submit_button(label='Calculate Optimal Discount')

# Mimic processing after hitting the button
if predict_button:
    with st.spinner('Calculating...'):
        time.sleep(2)  # Simulate a short processing time
    st.write("### Optimal Discount: 35%")
