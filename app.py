import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Startup Budget Tracker", layout="centered")
st.title("📊 Startup Budgeting App for IV Drip Monitor")

st.markdown("Input prices for each component. You can download the budget as a PDF to submit to your professor.")

# Predefined list
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

if "products" not in st.session_state:
    st.session_state["products"] = [{"Product": name, "Price": 0.0} for name in initial_products]

# Editable table
df = pd.DataFrame(st.session_state.products)
edited_df = st.data_editor(df, num_rows="dynamic", key="editable_products")

# Save changes
st.session_state.products = edited_df.to_dict(orient="records")

# Show total
total = edited_df["Price"].sum()
st.success(f"💰 Total Estimated Budget: SGD {total:.2f}")

# PDF export
def generate_pdf(df, total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Startup IV Drip Monitor Budget Report", ln=True, align='C')
    pdf.ln(10)
    for idx, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Product']}: SGD {row['Price']:.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Budget: SGD {total:.2f}", ln=True)
    return pdf.output(dest='S').encode('latin1')

pdf_bytes = generate_pdf(edited_df, total)
st.download_button("📥 Download Budget PDF", data=pdf_bytes, file_name="iv_drip_budget.pdf", mime="application/pdf")
