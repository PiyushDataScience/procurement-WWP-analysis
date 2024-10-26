import streamlit as st
import streamlit.components.v1 as components

def load_html_template():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Procurement Analysis - Schneider Electric</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/gsap.min.js"></script>
        <style>
            :root {
                --schneider-green: #3DCD58;
                --schneider-dark: #1A1A1A;
            }
            
            body {
                background-color: var(--schneider-dark);
                color: #ffffff;
            }

            .se-gradient {
                background: linear-gradient(135deg, #3DCD58 0%, #2A8E3C 100%);
            }

            .glow-effect {
                box-shadow: 0 0 15px rgba(61, 205, 88, 0.3);
                transition: all 0.3s ease;
            }

            .glow-effect:hover {
                box-shadow: 0 0 30px rgba(61, 205, 88, 0.5);
            }

            .se-card {
                background: rgba(26, 26, 26, 0.95);
                border: 1px solid rgba(61, 205, 88, 0.2);
                backdrop-filter: blur(10px);
            }

            .hexagon-bg {
                background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 5L55 20V40L30 55L5 40V20L30 5Z' fill='none' stroke='rgba(61, 205, 88, 0.1)' stroke-width='1'/%3E%3C/svg%3E");
                background-size: 60px 60px;
            }

            /* Hide Streamlit elements */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display: none;}
            
            /* Override Streamlit defaults */
            .stApp {
                background: none;
            }

            /* Custom Streamlit Styling */
            .stSelectbox > div > div {
                background-color: #2A2A2A !important;
                border: 1px solid rgba(61, 205, 88, 0.3) !important;
                color: white !important;
                border-radius: 0.5rem !important;
            }

            .stSelectbox > div > div:hover {
                border-color: var(--schneider-green) !important;
            }

            /* File uploader styling */
            .stFileUploader > div {
                background: transparent !important;
                border: 2px dashed rgba(61, 205, 88, 0.3) !important;
                border-radius: 0.75rem !important;
                padding: 2rem !important;
                transition: all 0.3s ease !important;
            }

            .stFileUploader > div:hover {
                border-color: rgba(61, 205, 88, 0.6) !important;
            }

            .stFileUploader > div > div {
                text-align: center !important;
            }

            .stFileUploader > div > div > div {
                color: #3DCD58 !important;
            }

            /* Button styling */
            .stButton > button {
                width: 100% !important;
                background: linear-gradient(135deg, #3DCD58 0%, #2A8E3C 100%) !important;
                color: white !important;
                border: none !important;
                padding: 1rem 2rem !important;
                font-weight: 500 !important;
                border-radius: 0.5rem !important;
                transition: all 0.3s ease !important;
                text-transform: none !important;
            }

            .stButton > button:hover {
                box-shadow: 0 0 30px rgba(61, 205, 88, 0.5) !important;
                transform: scale(1.05) !important;
            }

            /* Success message styling */
            .stSuccess {
                background-color: rgba(61, 205, 88, 0.1) !important;
                border: 1px solid rgba(61, 205, 88, 0.3) !important;
                color: white !important;
            }

            /* Spinner styling */
            .stSpinner > div {
                border-color: #3DCD58 !important;
            }
        </style>
    </head>
    <body class="min-h-screen hexagon-bg">
        <!-- Navigation Bar -->
        <nav class="bg-[#1A1A1A] border-b border-[#3DCD58]/20 p-4">
            <div class="container mx-auto flex justify-between items-center">
                <div class="flex items-center space-x-4">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Schneider_Electric_2007.svg/2560px-Schneider_Electric_2007.svg.png" 
                         alt="Schneider Electric Logo" class="h-10">
                    <span class="text-xl font-bold text-white">Procurement Analytics</span>
                </div>
                <div class="flex items-center space-x-6">
                    <a href="#" class="text-gray-300 hover:text-[#3DCD58] transition-colors">Dashboard</a>
                    <a href="#" class="text-gray-300 hover:text-[#3DCD58] transition-colors">History</a>
                    <a href="#" class="text-gray-300 hover:text-[#3DCD58] transition-colors">Help</a>
                </div>
            </div>
        </nav>
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

    # Inject custom HTML and CSS
    components.html(load_html_template(), height=0, width=0)

    # Main content
    st.markdown("""
        <div class="text-center mb-12 animate__animated animate__fadeIn">
            <h1 class="text-4xl font-bold mb-4">Procurement Analysis Tool</h1>
            <p class="text-gray-400">Powered by India Effectiveness Team</p>
        </div>
    """, unsafe_allow_html=True)

    # Center column layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="se-card rounded-xl p-8 glow-effect">
                <h2 class="text-3xl font-bold mb-8 text-[#3DCD58]">New Analysis</h2>
            </div>
        """, unsafe_allow_html=True)

        # Analysis Type Selection
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Select an analysis...", "Open PO Analysis", "WWP Analysis", "Rejected Part Analysis"],
            key="analysis_type"
        )

        if analysis_type != "Select an analysis...":
            st.markdown("""
                <div class="animate__animated animate__fadeIn">
                    <h3 class="text-xl font-medium text-[#3DCD58] mb-3">Required Files:</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Show required files based on analysis type
            if analysis_type == "Open PO Analysis":
                st.markdown("""
                    <ul class="list-disc pl-6 text-gray-400 space-y-2 text-lg">
                        <li>Open PO Report (.xlsx or .csv)</li>
                        <li>Workbench File (.xlsx or .csv)</li>
                    </ul>
                """, unsafe_allow_html=True)
            elif analysis_type == "WWP Analysis":
                st.markdown("""
                    <ul class="list-disc pl-6 text-gray-400 space-y-2 text-lg">
                        <li>CAP Base Report (.xlsx or .csv)</li>
                    </ul>
                """, unsafe_allow_html=True)
            elif analysis_type == "Rejected Part Analysis":
                st.markdown("""
                    <ul class="list-disc pl-6 text-gray-400 space-y-2 text-lg">
                        <li>PDM ZIP File (.zip)</li>
                    </ul>
                """, unsafe_allow_html=True)

            # File uploader with custom styling
            uploaded_files = st.file_uploader(
                "Drop your file(s) here or click to upload",
                accept_multiple_files=True,
                type=['xlsx', 'csv', 'zip'],
                help="Supported formats: .xlsx, .csv, .zip"
            )

            if uploaded_files:
                st.markdown("""
                    <div class="animate__animated animate__fadeIn">
                        <h3 class="text-xl font-medium text-[#3DCD58] mb-3">Uploaded Files:</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                for file in uploaded_files:
                    st.markdown(f"""
                        <div class="text-gray-400 text-lg">• {file.name}</div>
                    """, unsafe_allow_html=True)
                
                if st.button("Run Analysis", key="run_analysis"):
                    with st.spinner('Processing your analysis...'):
                        # Add your analysis logic here
                        st.success('Analysis completed successfully!')

if __name__ == "__main__":
    main()
