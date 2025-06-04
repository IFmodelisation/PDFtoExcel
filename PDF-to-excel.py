import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PDF to Excel Converter", layout="centered")

st.title("📄 PDF to Excel Converter")
st.write("Upload a PDF containing tables, and download the data as an Excel file.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

def extract_tables_from_pdf(pdf_file):
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            page_tables = page.extract_tables()
            for table in page_tables:
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = clean_data(df)
                    df.insert(0, "Page", i + 1)
                    tables.append(df)
    return tables

def clean_data(df):
    for col in df.columns:
        df[col] = df[col].str.replace(",", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors="ignore")
    return df

def save_tables_to_excel(tables):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for i, df in enumerate(tables):
            sheet_name = f"Table_{i+1}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output

if uploaded_file:
    st.info("Processing PDF...")
    tables = extract_tables_from_pdf(uploaded_file)

    if tables:
        excel_file = save_tables_to_excel(tables)

        st.success("Tables extracted and Excel file ready!")

        st.download_button(
            label="📥 Download Excel File",
            data=excel_file,
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No tables found in the PDF.")

