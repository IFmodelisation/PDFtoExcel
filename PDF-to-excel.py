import streamlit as st
import camelot
import pandas as pd
import io

# Function to extract tables from PDF using Camelot
def extract_tables_from_pdf(pdf_file):
    # Use Camelot to read the tables from the PDF
    tables = camelot.read_pdf(pdf_file, pages='all', flavor='stream')
    
    # If tables were found, convert them to DataFrames
    if len(tables) > 0:
        dfs = [table.df for table in tables]
        return dfs
    else:
        return None

# Function to save DataFrames to Excel
def save_to_excel(dfs):
    # Create a BytesIO object to hold the Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for i, df in enumerate(dfs):
            df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
    output.seek(0)
    return output

# Streamlit App
def main():
    st.title("PDF to Excel Converter with Camelot")
    
    # Allow the user to upload a PDF file
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        # Show a loading message while extracting data
        st.write("Extracting tables from PDF...")
        
        # Extract tables using Camelot
        tables = extract_tables_from_pdf(uploaded_file)
        
        if tables:
            # Show extracted tables
            st.write(f"Found {len(tables)} tables in the PDF.")
            for i, table in enumerate(tables):
                st.subheader(f"Table {i+1}")
                st.dataframe(table)  # Display the table as a dataframe
            
            # Provide the option to download the extracted data as an Excel file
            st.write("Click below to download the tables as an Excel file:")
            excel_file = save_to_excel(tables)
            st.download_button(
                label="Download Excel",
                data=excel_file,
                file_name="extracted_tables.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.write("No tables found in the PDF.")
            
if __name__ == "__main__":
    main()



