import camelot
import pandas as pd
import streamlit as st

# Streamlit file uploader
st.title("PDF Table Extraction to Excel")
st.markdown("Upload a PDF file to extract tables and save as an Excel file.")

# File upload widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Process the PDF if a file is uploaded
if uploaded_file is not None:
    try:
        # Use Camelot to extract tables from the uploaded PDF
        st.write("Extracting tables from the uploaded PDF...")
        tables = camelot.read_pdf(uploaded_file, pages='all', flavor='stream')

        # Check if tables were extracted
        if tables:
            st.write(f"Found {len(tables)} tables.")
            
            # Convert extracted tables into a list of DataFrames (one for each table)
            table_data = [table.df for table in tables]

            # Display the first table in the Streamlit app
            st.write("Here is the first extracted table:")
            st.dataframe(table_data[0])

            # Option to download as Excel
            st.write("Saving tables to Excel...")

            # Save all tables to Excel
            with pd.ExcelWriter("extracted_tables.xlsx", engine="openpyxl") as writer:
                for idx, table_df in enumerate(table_data):
                    table_df.to_excel(writer, sheet_name=f'Table_{idx + 1}', index=False)
            
            # Read the generated Excel file and make it available for download
            with open("extracted_tables.xlsx", "rb") as file:
                st.download_button(
                    label="Download the Excel file",
                    data=file,
                    file_name="extracted_tables.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("No tables found in the PDF.")

    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {e}")





