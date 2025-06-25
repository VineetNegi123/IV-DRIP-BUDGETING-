import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# Set Streamlit page config
st.set_page_config(page_title="IV Drip Budgeting App", layout="centered")

st.markdown("""
    <div style="background-color:#f5f5f5;padding:20px 0;">
        <h2 style="text-align:center; color:#003366; font-weight:bold; margin-bottom:0;">Budget Report</h2>
        <h4 style="text-align:center; color:#333333; font-weight:normal;">Project: IV Drip Monitoring System</h4>
    </div>
    """, unsafe_allow_html=True)

# Initial product list
initial_data = {
    "Product": [
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
    ],
    "Price": [0.00] * 10
}

df = pd.DataFrame(initial_data)

# Editable price inputs
for i in range(len(df)):
    df.at[i, "Price"] = st.number_input(
        f"Enter price for {df.at[i, 'Product']}",
        min_value=0.0,
        format="%.2f",
        key=f"price_{i}"
    )

total = df["Price"].sum()

st.markdown("---")
st.markdown(f"### 💰 Total Budget: SGD {total:.2f}")

# PDF generation function
def generate_pdf(df, total):
    pdf = FPDF()
    pdf.add_page()

    # Header bar
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(0, 0, 210, 20, 'F')
    pdf.set_xy(10, 8)
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Budget Report", ln=True, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Project: IV Drip Monitoring System", ln=True, align='C')
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(220, 220, 220)
    pdf.set_text_color(0)
    pdf.cell(140, 10, "Component", border=1, fill=True)
    pdf.cell(40, 10, "Price (SGD)", border=1, ln=True, fill=True)

    # Table Rows with alternating fill
    pdf.set_font("Arial", "", 11)
    for idx, row in df.iterrows():
        fill = idx % 2 == 0
        pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(140, 10, row["Product"], border="LR", fill=True)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(40, 10, f"{row['Price']:.2f}", border="LR", ln=True, fill=True)
        pdf.set_font("Arial", "", 11)

    # Bottom line
    pdf.cell(140, 0, "", border="T")
    pdf.cell(40, 0, "", border="T", ln=True)

    # Total row
    pdf.ln(6)
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(140, 10, "Total Budget", border=1, fill=True)
    pdf.set_text_color(0, 102, 0)
    pdf.cell(40, 10, f"SGD {total:.2f}", border=1, fill=True, ln=True)

    return pdf.output(dest='S').encode('latin1')

# Download button
if st.button("📄 Generate PDF Report"):
    pdf_bytes = generate_pdf(df, total)
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="iv_drip_budget_report.pdf">📥 Download Budget Report PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
