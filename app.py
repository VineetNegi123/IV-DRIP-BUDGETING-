import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- Page Setup ---
st.set_page_config(page_title="IV Drip Monitor Budget", layout="wide")

# --- Header ---
st.markdown(
    "<h1 style='margin-bottom: 0;'>Budgeting App for IV Drip Monitor</h1>"
    "<p style='color: gray; margin-top: 0;'>For internal business proposal and funding submission</p>",
    unsafe_allow_html=True,
)

# --- Initial Component List ---
initial_products = [
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

# Initialize only once
if "initialized" not in st.session_state:
    st.session_state["initialized"] = True
    st.session_state["df"] = pd.DataFrame(
        [{"Product": name, "Price": 0.0} for name in initial_products]
    )

# Editable DataFrame
st.markdown("### 🧾 Budget Entry Table")
st.markdown("Enter the expected price for each item below.")

edited_df = st.data_editor(
    st.session_state["df"],
    use_container_width=True,
    key="budget_editor"
)

# Budget summary
total = edited_df["Price"].sum()
st.markdown("---")
st.subheader("💰 Total Estimated Budget")
st.markdown(f"<h2 style='color: green;'>SGD {total:.2f}</h2>", unsafe_allow_html=True)

# --- PDF Generator ---
def generate_pdf(df, total):
    pdf = FPDF()
    pdf.add_page()

    # Header Bar (light gray background)
    pdf.set_fill_color(245, 245, 245)  # Soft gray
    pdf.rect(0, 0, 210, 20, 'F')

    # Title
    pdf.set_xy(10, 8)
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Budget Report", ln=True, align='C')
    pdf.set_font("Arial", "", 13)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, "Project: IV Drip Monitoring System", ln=True, align='C')
    pdf.ln(10)

    # Table Header
    pdf.set_fill_color(220, 220, 220)
    pdf.set_text_color(0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(140, 10, "Component", border=1, fill=True)
    pdf.cell(40, 10, "Price (SGD)", border=1, ln=True, fill=True)

    # Table Rows
    pdf.set_font("Arial", "", 11)
    for _, row in df.iterrows():
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(140, 10, row["Product"], border="LR")
        pdf.set_font("Arial", "B", 11)
        pdf.cell(40, 10, f"{row['Price']:.2f}", border="LR", ln=True)
        pdf.set_font("Arial", "", 11)

    # Bottom border
    pdf.cell(140, 0, "", border="T")
    pdf.cell(40, 0, "", border="T", ln=True)

    # Total
    pdf.ln(8)
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(140, 10, "Total Budget", border=1, fill=True)
    pdf.set_text_color(0, 102, 0)
    pdf.cell(40, 10, f"SGD {total:.2f}", border=1, fill=True, ln=True)

    return pdf.output(dest='S').encode('latin1')

# Download button
pdf_bytes = generate_pdf(edited_df, total)
st.download_button("📥 Download PDF Report", data=pdf_bytes, file_name="iv_drip_budget.pdf", mime="application/pdf")
