import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# Set page config
st.set_page_config(page_title="IV Drip Budget Tool", layout="centered")

# Page title
st.markdown("<h1 style='text-align: center; color: #0A2940;'>Budget Report</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Project: IV Drip Monitoring System</h4><br>", unsafe_allow_html=True)

# Product list
products = [
    "ESP32 S3",
    "Break beam sensor / Reflector sensor",
    "Optical sensor (air bubble detection)",
    "Lithium battery (backup power)",
    "LED (low drip night alert)",
    "IV drip stand",
    "Load sensor",
    "3D printed casing (transparent)",
    "Buzzer",
    "LED screen (optional)"
]

# User input for pricing
st.write("### Enter Prices (SGD):")
prices = []
for product in products:
    price = st.number_input(f"{product}", min_value=0.0, format="%.2f", key=product)
    prices.append(price)

# Prepare DataFrame and Total
df = pd.DataFrame({"Component": products, "Price (SGD)": prices})
total_budget = sum(prices)

# Generate PDF
if st.button("📄 Generate PDF Proposal"):

    class PDF(FPDF):
        def header(self):
            self.set_fill_color(232, 240, 255)
            self.set_text_color(0, 60, 120)
            self.set_font("Arial", "B", 16)
            self.cell(0, 12, "Budget Report", border=0, ln=1, align="C", fill=True)
            self.set_font("Arial", "", 12)
            self.set_text_color(50, 50, 50)
            self.cell(0, 10, "Project: IV Drip Monitoring System", ln=1, align="C")
            self.ln(6)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(130, 10, "Component", border=1, fill=True)
    pdf.cell(50, 10, "Price (SGD)", border=1, ln=1, fill=True)

    pdf.set_font("Arial", "", 11)
    for product, price in zip(products, prices):
        pdf.cell(130, 10, product, border=1)
        pdf.cell(50, 10, f"{price:.2f}", border=1, ln=1)

    # Total row
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(130, 10, "Total Budget", border=1, fill=True)
    pdf.cell(50, 10, f"SGD {total_budget:.2f}", border=1, ln=1, fill=True)

    # Output to buffer
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    buffer.name = "iv_drip_budget_proposal.pdf"
    buffer.seek(0)

    # Download button
    st.download_button(
        label="⬇️ Download PDF",
        data=buffer,
        file_name="iv_drip_budget_proposal.pdf",
        mime="application/pdf"
    )
