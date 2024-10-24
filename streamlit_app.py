import streamlit as st
from PIL import Image
from fpdf import FPDF
import base64

# Set the page configuration (title and favicon)
st.set_page_config(
    page_title="Aravally App Store",
    page_icon="favicon.ico"
)

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
banner_img = Image.open('Banner.png')
sieve_icon = Image.open('sieve_icon.png')  # Placeholder for Sieve Shaker icon
dal_icon = Image.open('dal_icon.png')      # Placeholder for Dal Split icon

# Define session state to manage navigation between screens
if 'screen' not in st.session_state:
    st.session_state.screen = 'home'

# Function to navigate to a specific screen
def navigate_to(screen):
    st.session_state.screen = screen

# Home Screen: Displays icons for navigation
if st.session_state.screen == 'home':
    st.image(banner_img, caption='', width=150)
    st.header("Welcome to Aravally App Store")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Sieve Shaker Calculator"):
            navigate_to('sieve')

        st.image(sieve_icon, caption='Sieve Shaker', width=120)

    with col2:
        if st.button("Dal Split Calculator"):
            navigate_to('dal')

        st.image(dal_icon, caption='Dal Split', width=120)

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

    if st.button("Back to Home"):
        navigate_to('home')

# Dal Split Calculator Screen
if st.session_state.screen == 'dal':
    st.header("Dal Split Calculator")

    date = st.text_input("Enter Date:")
    vehicle_number = st.text_input("Enter Vehicle Number:")
    party_name = st.text_input("Enter Party Name:")
    gaadi_type = st.radio("Select Gaadi Type:", options=["Khadi", "Poori"])

    weights = {}
    weight_labels = ["Daal", "Tukdi", "Red/Black", "Chhala", "Dankhal", "14 Mesh"]
    for label in weight_labels:
        weights[label] = st.number_input(f"Enter {label}:", min_value=0.000, step=0.001, format="%.3f")

    total_weight = round(sum(weights.values()), 3)
    doubled_weights = {k: round(v * 2, 3) for k, v in weights.items()}
    grand_total = round(sum(doubled_weights.values()), 3)

    percentages = {k: round(v * 10, 3) for k, v in doubled_weights.items()}
    dal_tukdi_percent = round(percentages["Daal"] + percentages["Tukdi"], 3)
    other_percent = round(sum(percentages.values()) - dal_tukdi_percent, 3)
    total_percent = round(dal_tukdi_percent + other_percent, 3)

    st.subheader("Grand Total")
    st.write(f"Grand Total: {total_weight}")

    st.subheader("Details for Sheet")
    for label, value in doubled_weights.items():
        st.write(f"{label}: {value}")
    st.write(f"Grand Total for Sheet: {grand_total}")

    st.subheader("Details in Percentage")
    for label, value in percentages.items():
        st.write(f"{label}: {value}%")
    st.write(f"Total (Dal + Tukdi): {dal_tukdi_percent}%")
    st.write(f"Total (Others): {other_percent}%")
    st.write(f"Overall Total: {total_percent}%")

    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.image('Banner.png', x=160, y=10, w=40)

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Dal Split Report", ln=True, align='C')
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
        pdf.cell(200, 10, txt=f"Vehicle Number: {vehicle_number}", ln=True)
        pdf.cell(200, 10, txt=f"Party Name: {party_name}", ln=True)
        pdf.cell(200, 10, txt=f"Gaadi Type: {gaadi_type}", ln=True)
        pdf.ln(10)

        pdf.cell(200, 10, txt="Details (in grams):", ln=True)
        for label, value in doubled_weights.items():
            pdf.cell(200, 10, txt=f"{label}: {value}gm", ln=True)
        pdf.cell(200, 10, txt=f"Grand Total for Sheet: {grand_total}gm", ln=True)
        pdf.ln(10)

        pdf.cell(200, 10, txt="Details (in percentage):", ln=True)
        for label, value in percentages.items():
            pdf.cell(200, 10, txt=f"{label}: {value}%", ln=True)
        pdf.cell(200, 10, txt=f"Total (Dal + Tukdi): {dal_tukdi_percent}%", ln=True)
        pdf.cell(200, 10, txt=f"Total (Others): {other_percent}%", ln=True)
        pdf.cell(200, 10, txt=f"Overall Total: {total_percent}%", ln=True)

        pdf_file = "dal_split_report.pdf"
        pdf.output(pdf_file)
        return pdf_file

    def pdf_download_link(pdf_file):
        with open(pdf_file, "rb") as f:
            pdf_data = f.read()
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="dal_split_report.pdf">📥 Download PDF</a>'
        return href

    if st.button("Generate PDF"):
        pdf_file = generate_pdf()
        st.markdown(pdf_download_link(pdf_file), unsafe_allow_html=True)

    if st.button("Back to Home"):
        navigate_to('home')
