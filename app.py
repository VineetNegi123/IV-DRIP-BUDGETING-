import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Startup Budget Tracker", layout="centered")

st.title("📊 Startup Product Budgeting App")

st.markdown("Enter product names and their prices below. You can export the budget as a PDF to share.")

if "products" not in st.session_state:
    st.session_state["products"] = []

with st.form("add_product_form", clear_on_submit=True):
    product_name = st.text_input("Product Name")
    product_price = st.number_input("Price (in SGD)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Product")

    if submitted and product_name:
        st.session_state.products.append({"Product": product_name, "Price": product_price})

# Show table
df = pd.DataFrame(st.session_state.products)
if not df.empty:
    st.subheader("🧾 Budget Table")
    st.dataframe(df, use_container_width=True)

    total = df["Price"].sum()
    st.success(f"💰 Total Budget: SGD {total:.2f}")

    # Download PDF
    def generate_pdf(df, total):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Startup Product Budget Report", ln=True, align='C')
        pdf.ln(10)
        for idx, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Product']}: SGD {row['Price']:.2f}", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Total: SGD {total:.2f}", ln=True)
        return pdf.output(dest='S').encode('latin1')

    pdf_bytes = generate_pdf(df, total)
    st.download_button("📥 Download Budget PDF", data=pdf_bytes, file_name="startup_budget.pdf", mime="application/pdf")

    st.caption("You can also right-click and Print to share it with your professor.")
else:
    st.info("Add a product to start budgeting.")
