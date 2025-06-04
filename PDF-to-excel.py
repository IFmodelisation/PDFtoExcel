import streamlit as st
import tabula
import pandas as pd
from io import BytesIO

# Configuration Streamlit
st.set_page_config(page_title="PDF to Excel Converter", layout="centered")

st.title("📄 PDF to Excel Converter")
st.write("Téléchargez un PDF contenant des tableaux financiers et téléchargez les données sous forme de fichier Excel.")

uploaded_file = st.file_uploader("Choisir un fichier PDF", type=["pdf"])

def extract_tables_from_pdf(pdf_file):
    tables = []
    try:
        # Lire les tableaux à partir du PDF (toutes les pages)
        tables = tabula.read_pdf(pdf_file, pages="all", multiple_tables=True, lattice=True)
        if not tables:
            raise ValueError("Aucun tableau trouvé dans le PDF.")
    except Exception as e:
        st.error(f"Erreur lors de l'extraction des tableaux : {str(e)}")
    
    return tables

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
        # Extraction des tableaux avec tabula-py
        tables = extract_tables_from_pdf(uploaded_file)

        if tables:
            # Sauvegarder les tableaux extraits sous forme de fichier Excel
            excel_file = save_tables_to_excel(tables)

            st.success("Les tableaux ont été extraits et le fichier Excel est prêt!")

            # Ajouter un bouton de téléchargement pour le fichier Excel
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
    


