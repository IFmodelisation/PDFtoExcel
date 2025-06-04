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
                    # Directly create the DataFrame without any data cleaning
                    df = pd.DataFrame(table




