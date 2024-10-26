import streamlit as st
import base64
from pathlib import Path
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Procurement Analysis - Schneider Electric",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match the original design
css = """
<style>
    /* Main theme colors and styles */
    :root {
        --schneider-green: #3DCD58;
        --schneider-dark: #1A1A1A;
    }
    
    /* Override Streamlit's default styles */
    .stApp {
        background-color: var(--schneider-dark);
    }
    
    .stSelectbox > div > div {
        background-color: #2A2A2A !important;
        border: 1px solid rgba(61, 205, 88, 0.3) !important;
        color: white !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #3DCD58 !important;
    }
    
    /* Custom card style */
    .se-card {
        background: rgba(26, 26, 26, 0.95);
        border: 1px solid rgba(61, 205, 88, 0.2);
        border-radius: 1rem;
        padding: 2rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Navigation bar style */
    .navbar {
        background-color: #1A1A1A;
        border-bottom: 1px solid rgba(61, 205, 88, 0.2);
        padding: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .nav-links {
        display: flex;
        gap: 1.5rem;
    }
    
    .nav-link {
        color: #9CA3AF;
        text-decoration: none;
        transition: color 0.3s;
    }
    
    .nav-link:hover {
        color: #3DCD58;
    }
    
    /* File uploader custom style */
    .uploadfield {
        border: 2px dashed rgba(61, 205, 88, 0.3);
        border-radius: 0.75rem;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s;
    }
    
    .uploadfield:hover {
        border-color: rgba(61, 205, 88, 0.6);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3DCD58 0%, #2A8E3C 100%);
        color: white;
        width: 100%;
        padding: 0.75rem 1.5rem;
        font-size: 1.25rem;
        font-weight: 500;
        border: none;
        border-radius: 0.5rem;
        transition: transform 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
    }
    
    /* Text colors */
    .green-text {
        color: #3DCD58;
    }
    
    .gray-text {
        color: #9CA3AF;
    }
</style>
"""

# Navigation bar HTML
navbar = """
<div class="navbar">
    <div class="nav-brand">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Schneider_Electric_2007.svg/2560px-Schneider_Electric_2007.svg.png" 
             alt="Schneider Electric Logo" style="height: 2.5rem;">
        <span style="color: white; font-size: 1.25rem; font-weight: bold;">Procurement Analytics</span>
    </div>
    <div class="nav-links">
        <a href="#" class="nav-link">Dashboard</a>
        <a href="#" class="nav-link">History</a>
        <a href="#" class="nav-link">Help</a>
    </div>
</div>
<div style="height: 5rem;"></div>
"""

# Inject custom CSS and navbar
st.markdown(css, unsafe_allow_html=True)
st.markdown(navbar, unsafe_allow_html=True)

# Main content
st.markdown('<div class="se-card">', unsafe_allow_html=True)

# Title and subtitle
st.markdown('<h1 style="text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem;">Procurement Analysis Tool</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #9CA3AF; margin-bottom: 2rem;">Powered by India Effectiveness Team</p>', unsafe_allow_html=True)

# Analysis type selection
st.markdown('<h2 class="green-text" style="font-size: 1.875rem; font-weight: bold; margin-bottom: 2rem;">New Analysis</h2>', unsafe_allow_html=True)
analysis_type = st.selectbox(
    "Select Analysis Type",
    ["Select an analysis...", "Open PO Analysis", "WWP Analysis", "Rejected Part Analysis"],
    key="analysis_type"
)

# Show file upload instructions based on selection
if analysis_type != "Select an analysis...":
    st.markdown('<h3 class="green-text" style="font-size: 1.25rem; margin-top: 2rem;">Required Files:</h3>', unsafe_allow_html=True)
    
    if analysis_type == "Open PO Analysis":
        required_files = ["Open PO Report (.xlsx or .csv)", "Workbench File (.xlsx or .csv)"]
    elif analysis_type == "WWP Analysis":
        required_files = ["CAP Base Report (.xlsx or .csv)"]
    else:  # Rejected Part Analysis
        required_files = ["PDM ZIP File (.zip)"]
    
    for file in required_files:
        st.markdown(f'<li class="gray-text" style="margin-left: 1.5rem;">{file}</li>', unsafe_allow_html=True)
    
    # File upload section
    st.markdown('<div class="uploadfield" style="margin-top: 2rem;">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Drop your file(s) here or click to upload", 
                                    accept_multiple_files=True,
                                    type=['xlsx', 'csv', 'zip'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display uploaded files
    if uploaded_files:
        st.markdown('<h3 class="green-text" style="font-size: 1.25rem; margin-top: 2rem;">Uploaded Files:</h3>', unsafe_allow_html=True)
        for file in uploaded_files:
            st.markdown(f'<li class="gray-text" style="margin-left: 1.5rem;">{file.name}</li>', unsafe_allow_html=True)
        
        # Submit button
        if st.button("Run Analysis"):
            with st.spinner('Processing your analysis...'):
                # Add your analysis logic here
                st.success('Analysis completed successfully!')

st.markdown('</div>', unsafe_allow_html=True)
