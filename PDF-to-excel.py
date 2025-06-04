import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PDF to Excel Converter", layout="centered")

st.title("📄 PDF to Excel Converter")
st.write("Téléchargez un PDF contenant des tableaux et téléchargez les données sous forme de fichier Excel.")

uploaded_file = st.file_uploader("Choisir un fichier PDF", type=["pdf"])

def extract_tables_from_pdf(pdf_file):
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            st.write(f"Analyse de la page {i+1}...")
            
            # Afficher un aperçu du texte extrait pour diagnostic
            page_text = page.extract_text()
            st.text_area(f"Texte extrait de la page {i+1}", page_text, height=200)

            # Extraire les tables avec un réglage de détection amélioré
            page_tables = page.extract_tables(
                table_settings={
                    "vertical_strategy": "text",  # Utiliser la stratégie de texte pour détecter les lignes de texte
                    "horizontal_strategy": "text",  # Utiliser la stratégie de texte pour détecter les colonnes
                    "snap_tolerance": 3,  # Ajustement de la tolérance de capture des lignes et colonnes
                }
            )

            # Afficher le nombre de tableaux trouvés
            if page_tables:
                st.write(f"{len(page_tables)} tableaux trouvés sur la page {i+1}.")
            
            # Afficher chaque tableau brut extrait pour analyse
            for table in page_tables:
                st.write(f"Tableau brut extrait de la page {i+1}:")
                st.write(table)

            # Ajouter de nouveaux tableaux extraits à la liste
            for table in page_tables:
                if table:  # Si un tableau n'est pas vide
                    # Nettoyer les données du tableau
                    table_cleaned = clean_table(table)
                    if table_cleaned:  # Ajouter seulement les tableaux non vides
                        df = pd.DataFrame(table_cleaned[1:], columns=table_cleaned[0])  # Première ligne comme en-tête
                        df.insert(0, "Page", i + 1)  # Ajout de la colonne de la page
                        tables.append(df)

            # Afficher un exemple du dernier tableau extrait
            if tables:
                st.write(f"Exemple de tableau extrait de la page {i+1}:")
                st.write(tables[-1].head())  # Affiche les premières lignes du dernier tableau extrait
    
    return tables

def clean_table(table):
    """
    Fonction pour nettoyer les tables extraites en supprimant les colonnes vides ou dupliquées.
    """
    cleaned_table = []
    
    # Vérifier et nettoyer les lignes
    columns = table[0]
    cleaned_columns = [col if col != '' else f'Column_{i+1}' for i, col in enumerate(columns)]
    table[0] = cleaned_columns  # Remplacer les noms de colonnes vides par des noms génériques
    
    for row in table:
        cleaned_row = [cell.strip() if isinstance(cell, str) else cell for cell in row]  # Nettoyer les cellules
        if any(cleaned_row):  # Garder la ligne si elle n'est pas vide
            cleaned_table.append(cleaned_row)
    
    return cleaned_table

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
