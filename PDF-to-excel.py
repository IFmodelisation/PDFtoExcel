import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PDF to Excel Converter", layout="centered")

st.title("📄 PDF to Excel Converter")
st.write("Téléchargez un PDF contenant des tableaux, et téléchargez les données sous forme de fichier Excel.")

uploaded_file = st.file_uploader("Choisir un fichier PDF", type=["pdf"])

def extract_tables_from_pdf(pdf_file):
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            st.write(f"Analyse de la page {i+1}...")
            
            # Extraire les tables de la page avec un ajustement des paramètres
            page_tables = page.extract_tables(table_settings={"vertical_strategy": "text", "horizontal_strategy": "lines"})
            
            if page_tables:
                st.write(f"{len(page_tables)} tableaux trouvés sur la page {i+1}.")
                
            for table in page_tables:
                if table:  # Si le tableau n'est pas vide
                    df = pd.DataFrame(table[1:], columns=table[0])  # Utilisation de la première ligne comme en-têtes
                    df.insert(0, "Page", i + 1)  # Ajout de la page pour référence
                    tables.append(df)
            # Ajouter un petit délai pour que l'utilisateur voit le progrès
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
        tables = extract_tables_from_pdf(uploaded_file)

        if tables:
            excel_file = save_tables_to_excel(tables)

            st.success("Les tableaux ont été extraits et le fichier Excel est prêt!")

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

