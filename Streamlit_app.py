import streamlit as st
import pandas as pd
from analysis_logic import open_po_analysis, rejected_part_analysis, wwp_analysis

st.set_page_config(page_title="Procurement Analysis Tool", page_icon="📊")

st.title("Procurement Analysis Tool")
st.write("Powered by India Effectiveness Team")

analysis_type = st.selectbox("Select Analysis Type", ["Select an analysis...", "Open PO", "WWP", "Rejected Part"])

if analysis_type != "Select an analysis...":
    uploaded_files = st.file_uploader("Upload file(s)", type=["xlsx", "csv", "zip"], accept_multiple_files=True)
    
    if uploaded_files:
        # Load data from uploaded files and run analysis
        data_frames = []
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith('.csv'):
                data_frames.append(pd.read_csv(uploaded_file))
            elif uploaded_file.name.endswith('.xlsx'):
                data_frames.append(pd.read_excel(uploaded_file))
            # Add logic to handle ZIP files

        # Assuming you have functions in your analysis logic
        if analysis_type == "Open PO":
            result = open_po_analysis.run(data_frames)
            st.write(result)
        elif analysis_type == "WWP":
            result = wwp_analysis.run(data_frames)
            st.write(result)
        elif analysis_type == "Rejected Part":
            result = rejected_part_analysis.run(data_frames)
            st.write(result)
