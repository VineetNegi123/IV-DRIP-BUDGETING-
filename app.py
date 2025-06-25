import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image

# --- Page Setup ---
st.set_page_config(page_title="IV Drip Monitor Budget", layout="wide")

# --- Header with Logo ---
col1, col2 = st.columns([1, 8])
with col1:
    image = Image.open("logo.png")
    st.image(image, width=60)
with col2:
    st.markdown(
        "<h1 style='margin-bottom: 0;'>Startup Budgeting App for IV Drip Monitor</h1>"
        "<p style='color: gray; margin-top: 0;'>For internal startup proposal and funding submission</p>",
        unsafe_allow_html=True,
    )

# --- Component List ---
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

st.markdown("### 🧾 Budget Entry Table")
st.markdown("Enter the expected price for each item. This will be used to calculate your total budget estimate.")

# Editable DataFrame
df = pd.DataFrame(st.session_state["products"])
edited_df = st.data_editor(df, use_container_width=True, key="budget_table", num_rows="dynamic")
st.session_state["products"] = edited_df.to_dict(orient="records")

# --- Budget Summary ---
total = edited_df["Price"].sum()
st.markdown("---")
st.subheader("💰 Total Estimated Budget")
st.markdown(f"<h2 style='color: green;'>SGD {total:.2f}</h2>", unsafe_allow_html=True)

# --- PDF Generator ---
def generate_pdf(df, total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Startup Budget Report: IV Drip Monitor", ln=True, align='C')
    pdf.ln(10)
    for idx, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Product']}: SGD {row['Price']:.2f}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt=f"Total Budget: SGD {total:.2f}", ln=True)
    return pdf.output(dest='S').encode('latin1')

pdf_bytes = generate_pdf(edited_df, total)
st.download_button("📥 Download PDF Report", data=pdf_bytes, file_name="iv_drip_budget.pdf", mime="application/pdf")

st.caption("Generated for internal business proposal & review.")
