import streamlit as st
from PIL import Image
from fpdf import FPDF
import base64
import os

# Set the page configuration (title and favicon)
st.set_page_config(
    page_title="Aravally App Store",
    page_icon="favicon.ico"
)

# Inject JavaScript to modify the title
title_js = """
<script>
document.title = "Aravally App Store";
</script>
"""
st.markdown(title_js, unsafe_allow_html=True)

# Hide Streamlit's default UI components
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Load images for the welcome screen icons
banner_img = Image.open('Banner2.png')
sieve_icon = Image.open('sieve_icon.png')  # Placeholder for Sieve Shaker icon
dal_icon = Image.open('daal_icon.png')      # Placeholder for Dal Split icon

# trial starts
# Define session state to manage navigation between screens
if 'screen' not in st.session_state:
    st.session_state.screen = 'home'

# Function to navigate to a specific screen
def navigate_to(screen):
    st.session_state.screen = screen

# Home Screen: Displays icons for navigation
if st.session_state.screen == 'home':
    st.image(banner_img, caption='', width=200)
    st.header("Welcome to Aravally App Store")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Sieve Shaker Calculator"):
            navigate_to('sieve')

        st.image(sieve_icon, caption='', width=120)

    with col2:
        if st.button("Dal Split Calculator"):
            navigate_to('dal')

        st.image(dal_icon, caption='', width=120)

# Sieve Shaker Calculator Screen
if st.session_state.screen == 'sieve':
    st.header("Sieve Shaker Calculator")

    sample = st.number_input("Enter Sample:", min_value=1, step=1)

    sieve_inputs = []
    labels = ["60#", "100#", "150#", "200#", "240#", "300#", "350#", "Base"]
    for label in labels:
        value = st.number_input(f"Enter {label}:", min_value=0.000, step=0.001, format="%.3f")
        sieve_inputs.append(value)

    if sample > 0:
        cumulative = 0
        for idx, weight in enumerate(sieve_inputs):
            cumulative += (weight * 100) / sample
            st.write(f"{labels[idx]}: {cumulative:.4f}%")
    else:
        st.write("Please enter a sample greater than 0.")
