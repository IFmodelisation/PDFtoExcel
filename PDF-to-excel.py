import streamlit as st
import camelot
import pandas as pd
from io import BytesIO

# Configuration Streamlit
st.set_page_config(page_title="PDF to Excel Converter with Camelot", layout="centered")

st.title("📄 PDF to Excel Converter (Camelot)")
st.write("Téléchargez un PDF contenant des tableaux financiers et téléchargez les données sous forme de fichier Excel.")

# File uploader for PDF
uploaded_file = st.file_uploader("Choisir un fichier PDF", type=["pdf"])

def extract_tables_from_pdf(pdf_file):
    try:
        # Use Camelot to read the PDF and extract tables
        tables = camelot.read_pdf(pdf_file, pages="all", flavor="stream", edge_tol=500)
        
        if not tables:
            raise ValueError("Aucun tableau trouvé dans le PDF.")
        
        # Debug: Show how many tables were extracted
        st.write(f"{len(tables)} tableau(x) trouvé(s) dans le PDF.")
        
        # If tables are found, return them as a list of DataFrames
        return [table.df for table in tables]
    
    except Exception as e:
        st.error(f"Erreur lors de l'extraction des tableaux : {str(e)}")
        return []

def save_tables_to_excel(tables):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for i, df in enumerate(tables):
            sheet_name = f"Table_{i+1}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output

if uploaded_file:
    st.info("Traitement du PDF...")
    try:
        # Extract tables using Camelot
        tables = extract_tables_from_pdf(uploaded_file)

        if tables:
            # Save extracted tables into an Excel file
            excel_file = save_tables_to_excel(tables)

            st.success("Les tableaux ont été extraits et le fichier Excel est prêt!")

            # Add download button for the Excel file
            st.download_button(
                label="📥 Télécharger le fichier Excel",
                data=excel_file,
                file_name="extracted_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Aucun tableau n'a été trouvé dans le PDF.")
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")



