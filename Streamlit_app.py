import streamlit as st
import pandas as pd
from analysis_logic import open_po_analysis, rejected_part_analysis, wwp_analysis

st.set_page_config(page_title="Procurement Analysis Tool", page_icon="📊")

st.title("Procurement Analysis Tool")
st.write("Powered by India Effectiveness Team")

# Select analysis type
analysis_type = st.selectbox("Select Analysis Type", ["Select an analysis...", "Open PO", "WWP", "Rejected Part"])

# File uploader for data files
uploaded_files = st.file_uploader("Upload your files", type=["xlsx", "csv", "zip"], accept_multiple_files=True)

# Handle Open PO analysis
if analysis_type == "Open PO":
    if uploaded_files:
        # Check for at least two files (Open PO and WB)
        if len(uploaded_files) >= 2:
            open_po_file = uploaded_files[0]  # Assuming the first file is Open PO
            wb_file = uploaded_files[1]  # Assuming the second file is WB
            
            open_po_bef = pd.read_excel(open_po_file)  # Load Open PO file
            wb = pd.read_excel(wb_file)  # Load WB file
            
            if 'LINE_TYPE' in open_po_bef.columns:  # Ensure the required column exists
                result = open_po_analysis.run(open_po_bef, wb)  # Run analysis
                st.write(result)  # Display results
            else:
                st.error("Open PO file does not contain 'LINE_TYPE' column.")
        else:
            st.warning("Please upload at least two files: Open PO and WB.")

# Placeholder for WWP analysis
elif analysis_type == "WWP":
    if uploaded_files:
        # Extend this section to handle WWP analysis
        st.write("WWP analysis is under construction. Please check back later!")

# Placeholder for Rejected Part analysis
elif analysis_type == "Rejected Part":
    if uploaded_files:
        # Extend this section to handle Rejected Part analysis
        st.write("Rejected Part analysis is under construction. Please check back later!")

