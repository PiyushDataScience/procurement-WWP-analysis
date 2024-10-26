import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

def load_custom_css():
    return """
    <style>
        /* Root variables */
        :root {
            --schneider-green: #3DCD58;
            --schneider-dark: #1A1A1A;
        }
        
        /* Global styles */
        .main {
            background-color: var(--schneider-dark) !important;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
        }
        .stApp {
            background-color: var(--schneider-dark) !important;
        }
        
        /* Navigation styling */
        .nav-container {
            background-color: var(--schneider-dark);
            border-bottom: 1px solid rgba(61, 205, 88, 0.2);
            padding: 1rem;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .nav-links {
            display: flex;
            gap: 1.5rem;
        }
        
        .nav-link {
            color: #808080;
            text-decoration: none;
            transition: color 0.3s;
        }
        
        .nav-link:hover {
            color: var(--schneider-green);
        }
        
        /* Card styling */
        .se-card {
            background: rgba(26, 26, 26, 0.95);
            border: 1px solid rgba(61, 205, 88, 0.2);
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 0 15px rgba(61, 205, 88, 0.1);
            backdrop-filter: blur(10px);
            margin: 2rem 0;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #3DCD58 0%, #2A8E3C 100%) !important;
            color: white !important;
            border: none !important;
            padding: 1rem 2rem !important;
            border-radius: 0.5rem !important;
            font-weight: 500 !important;
            width: 100% !important;
            transition: transform 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: scale(1.05);
        }
        
        .stButton > button:disabled {
            opacity: 0.5;
            transform: none;
        }
        
        /* File uploader styling */
        .uploadedFile {
            background-color: #2A2A2A !important;
            border: 2px dashed rgba(61, 205, 88, 0.3) !important;
            border-radius: 0.5rem !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
        }
        
        .uploadedFile:hover {
            border-color: rgba(61, 205, 88, 0.6) !important;
        }
        
        /* Select box styling */
        .stSelectbox > div > div {
            background-color: #2A2A2A !important;
            border: 1px solid rgba(61, 205, 88, 0.3) !important;
            border-radius: 0.5rem !important;
            color: white !important;
        }
        
        .stSelectbox > div > div:hover {
            border-color: var(--schneider-green) !important;
        }
        
        /* Text styling */
        .title {
            color: white;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            color: #808080;
            text-align: center;
            font-size: 1.1rem;
        }
        
        .section-title {
            color: var(--schneider-green);
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Hexagon background */
        .hexagon-bg {
            background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 5L55 20V40L30 55L5 40V20L30 5Z' fill='none' stroke='rgba(61, 205, 88, 0.1)' stroke-width='1'/%3E%3C/svg%3E");
            background-size: 60px 60px;
        }
    </style>
    """

def get_base64_logo():
    # You would need to replace this with the actual Schneider Electric logo
    # For now, we'll use a placeholder SVG
    return """
    <svg width="200" height="50" viewBox="0 0 200 50">
        <rect width="200" height="50" fill="#3DCD58"/>
        <text x="20" y="30" fill="white" font-size="20">Schneider Electric</text>
    </svg>
    """

def main():
    # Page config
    st.set_page_config(
        page_title="Procurement Analysis - Schneider Electric",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Inject custom CSS
    st.markdown(load_custom_css(), unsafe_allow_html=True)

    # Navigation
    st.markdown(f"""
        <div class="nav-container">
            <div style="display: flex; align-items: center; gap: 1rem;">
                {get_base64_logo()}
                <span style="font-size: 1.5rem; font-weight: bold;">Procurement Analytics</span>
            </div>
            <div class="nav-links">
                <a href="#" class="nav-link">Dashboard</a>
                <a href="#" class="nav-link">History</a>
                <a href="#" class="nav-link">Help</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div class="title animate__animated animate__fadeIn">
            Procurement Analysis Tool
        </div>
        <div class="subtitle animate__animated animate__fadeIn">
            Powered by India Effectiveness Team
        </div>
    """, unsafe_allow_html=True)

    # Main content container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="se-card">', unsafe_allow_html=True)
            
            st.markdown('<h2 class="section-title">New Analysis</h2>', unsafe_allow_html=True)
            
            # Analysis Type Selection
            analysis_type = st.selectbox(
                "Select Analysis Type",
                ["Select an analysis...", "Open PO Analysis", "WWP Analysis", "Rejected Part Analysis"],
                key="analysis_type"
            )

            if analysis_type != "Select an analysis...":
                st.markdown('<h3 style="color: #3DCD58; margin-top: 1.5rem; font-size: 1.2rem;">Required Files:</h3>', unsafe_allow_html=True)
                
                if analysis_type == "Open PO Analysis":
                    st.markdown("""
                        * Open PO Report (.xlsx or .csv)
                        * Workbench File (.xlsx or .csv)
                    """)
                elif analysis_type == "WWP Analysis":
                    st.markdown("* CAP Base Report (.xlsx or .csv)")
                elif analysis_type == "Rejected Part Analysis":
                    st.markdown("* PDM ZIP File (.zip)")

                # File uploader with custom styling
                uploaded_files = st.file_uploader(
                    "Drop your file(s) here or click to upload",
                    accept_multiple_files=True,
                    type=['xlsx', 'csv', 'zip'],
                    help="Supported formats: .xlsx, .csv, .zip",
                    key="file_uploader"
                )

                if uploaded_files:
                    st.markdown('<h3 style="color: #3DCD58; margin-top: 1.5rem; font-size: 1.2rem;">Uploaded Files:</h3>', unsafe_allow_html=True)
                    for file in uploaded_files:
                        st.markdown(f"* {file.name}")
                    
                    if st.button("Run Analysis", key="run_analysis"):
                        with st.spinner('Processing your analysis...'):
                            # Add your analysis logic here
                            # For demonstration, we'll just show a success message
                            st.success('Analysis completed successfully!')

            st.markdown('</div>', unsafe_allow_html=True)

    # Add hexagon background
    st.markdown("""
        <div class="hexagon-bg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;"></div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
