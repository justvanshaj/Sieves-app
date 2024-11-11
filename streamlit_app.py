import streamlit as st
from PIL import Image
from fpdf import FPDF
import base64
import os

# Hide Streamlit's default UI components
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Define session state to manage navigation between screens
if 'screen' not in st.session_state:
    st.session_state.screen = 'home'

# Function to navigate to a specific screen
def navigate_to(screen):
    st.session_state.screen = screen

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
