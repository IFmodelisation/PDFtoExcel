import streamlit as st
import camelot
import pandas as pd
from io import BytesIO

# Function to extract tables with both 'stream' and 'lattice' flavors
def extract_tables(pdf_file, pages='all'):
    tables_stream = camelot.read_pdf(pdf_file, pages=pages, flavor='stream')
    tables_lattice = camelot.read_pdf(pdf_file, pages=pages, flavor='lattice')

    # Choose the flavor that returns more tables (as a simple heuristic)
    tables = tables_lattice if len(tables_lattice) > len(tables_stream) else tables_stream

    return tables

# Convert tables to Excel format
def tables_to_excel(tables):
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for i, table in enumerate(tables):
            df = table.df
            df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            df.to_excel(writer, index=False, sheet_name=f'Table_{i+1}')
    output.seek(0)
    return output

# Streamlit UI
def main():
    st.title('🧾 PDF to Excel Table Extractor')
    st.write("Upload a PDF and extract tables into an Excel file.")

    pdf_file = st.file_uploader("Upload PDF", type="pdf")
    pages = st.text_input("Pages to extract (e.g., '1,2,3' or 'all')", value="all")

    if pdf_file:
        st.info("Extracting tables... This may take a few seconds.")
        try:
            tables = extract_tables(pdf_file, pages)

            if len(tables) == 0:
                st.error("No tables were detected in the selected pages.")
                return

            # Display each table for preview
            for i, table in enumerate(tables):
                st.subheader(f"Preview of Table {i+1}")
                st.dataframe(table.df.head(10))

            # Convert and download
            output = tables_to_excel(tables)
            st.success(f"Successfully extracted {len(tables)} tables.")
            st.download_button(
                label="📥 Download Excel file",
                data=output,
                file_name="extracted_tables.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()







