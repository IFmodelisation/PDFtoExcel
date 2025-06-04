import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PDF to Excel Converter", layout="centered")

st.title("📄 PDF to Excel Converter")
st.markdown("Upload a PDF file, and we'll extract tables and convert them to an Excel file with correct number formatting.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

def convert_pdf_to_dfs(file):
    all_tables = []
    with pdfplumber.open(file) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table in tables:
                if table:  # skip empty
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = clean_and_convert_dataframe(df)
                    df.insert(0, 'Page', page_num)
                    all_tables.append(df)
    return all_tables

def clean_and_convert_dataframe(df):
    # Strip whitespaces and convert numeric values
    for col in df.columns:
        df[col] = df[col].str.replace(',', '').str.strip()  # Remove commas from numbers
        df[col] = pd.to_numeric(df[col], errors='ignore')   # Convert to numeric if possible
    return df

def create_excel_file(dfs):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for i, df in enumerate(dfs):
            sheet_name = f"Table_{i+1}"
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    output.seek(0)
    return output

if uploaded_file:
    with st.spinner("Extracting data from PDF..."):
        tables = convert_pdf_to_dfs(uploaded_file)

    if tables:
        excel_file = create_excel_file(tables)
        st.success("Data extracted and converted to Excel!")

        st.download_button(
            label="📥 Download Excel File",
            data=excel_file,
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No tables found in the uploaded PDF.")
