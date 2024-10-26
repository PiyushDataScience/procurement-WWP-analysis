# streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components

def load_html_template():
    """Load the HTML template for the custom UI"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Procurement Analysis - Schneider Electric</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
        <style>
            :root {
                --schneider-green: #3DCD58;
                --schneider-dark: #1A1A1A;
            }
            
            body {
                background-color: var(--schneider-dark);
                color: #ffffff;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            }

            .se-gradient {
                background: linear-gradient(135deg, #3DCD58 0%, #2A8E3C 100%);
            }

            .se-card {
                background: rgba(26, 26, 26, 0.95);
                border: 1px solid rgba(61, 205, 88, 0.2);
                box-shadow: 0 0 15px rgba(61, 205, 88, 0.1);
            }

            .hexagon-bg {
                background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 5L55 20V40L30 55L5 40V20L30 5Z' fill='none' stroke='rgba(61, 205, 88, 0.1)' stroke-width='1'/%3E%3C/svg%3E");
                background-size: 60px 60px;
            }
        </style>
    </head>
    <body class="min-h-screen hexagon-bg">
        <div id="streamlit_content"></div>
    </body>
    </html>
    """

def main():
    # Page config
    st.set_page_config(
        page_title="Procurement Analysis - Schneider Electric",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS
    st.markdown("""
        <style>
            .main {
                background-color: #1A1A1A;
            }
            .stApp {
                background-color: #1A1A1A;
            }
            
            /* Header styling */
            .header-container {
                background-color: #1A1A1A;
                border-bottom: 1px solid rgba(61, 205, 88, 0.2);
                padding: 1rem;
                margin-bottom: 2rem;
            }
            
            /* Card styling */
            .css-1r6slb0 {
                background-color: #1A1A1A;
                border: 1px solid rgba(61, 205, 88, 0.2);
                border-radius: 1rem;
                padding: 2rem;
                box-shadow: 0 0 15px rgba(61, 205, 88, 0.1);
            }
            
            /* Button styling */
            .stButton > button {
                background: linear-gradient(135deg, #3DCD58 0%, #2A8E3C 100%);
                color: white;
                border: none;
                padding: 0.75rem 2rem;
                border-radius: 0.5rem;
                font-weight: 500;
                width: 100%;
            }
            
            /* File uploader styling */
            .stUploadButton > button {
                background-color: transparent !important;
                border: 2px dashed rgba(61, 205, 88, 0.3) !important;
                color: #ffffff !important;
            }
            
            .stUploadButton:hover > button {
                border-color: rgba(61, 205, 88, 0.6) !important;
            }
            
            /* Select box styling */
            .stSelectbox > div > div {
                background-color: #2A2A2A;
                border: 1px solid rgba(61, 205, 88, 0.3);
            }
            
            /* Hide Streamlit branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Custom text colors */
            .green-text {
                color: #3DCD58;
            }
            
            .gray-text {
                color: #808080;
            }
        </style>
    """, unsafe_allow_html=True)

    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1 style='color: white; font-size: 2.5rem; margin-bottom: 0.5rem;'>Procurement Analysis Tool</h1>
                <p style='color: #808080;'>Powered by India Effectiveness Team</p>
            </div>
        """, unsafe_allow_html=True)

    # Main content
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h2 style='color: #3DCD58; font-size: 1.8rem; margin-bottom: 1rem;'>New Analysis</h2>", unsafe_allow_html=True)
            
            # Analysis Type Selection
            analysis_type = st.selectbox(
                "Select Analysis Type",
                ["Select an analysis...", "Open PO Analysis", "WWP Analysis", "Rejected Part Analysis"],
                key="analysis_type"
            )

            if analysis_type != "Select an analysis...":
                st.markdown("<h3 style='color: #3DCD58; margin-top: 1.5rem;'>Required Files:</h3>", unsafe_allow_html=True)
                
                if analysis_type == "Open PO Analysis":
                    st.markdown("""
                        * Open PO Report (.xlsx or .csv)
                        * Workbench File (.xlsx or .csv)
                    """)
                elif analysis_type == "WWP Analysis":
                    st.markdown("* CAP Base Report (.xlsx or .csv)")
                elif analysis_type == "Rejected Part Analysis":
                    st.markdown("* PDM ZIP File (.zip)")

                # File uploader
                uploaded_files = st.file_uploader(
                    "Drop your file(s) here or click to upload",
                    accept_multiple_files=True,
                    type=['xlsx', 'csv', 'zip'],
                    help="Supported formats: .xlsx, .csv, .zip"
                )

                if uploaded_files:
                    st.markdown("<h3 style='color: #3DCD58; margin-top: 1.5rem;'>Uploaded Files:</h3>", unsafe_allow_html=True)
                    for file in uploaded_files:
                        st.markdown(f"* {file.name}")
                    
                    if st.button("Run Analysis"):
                        with st.spinner('Processing your analysis...'):
                            # Add your analysis logic here
                            st.success('Analysis completed successfully!')

if __name__ == "__main__":
    main()
