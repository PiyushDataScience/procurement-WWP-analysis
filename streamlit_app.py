# streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components

def load_html_template():
    """Load the HTML template and inject necessary modifications for Streamlit"""
    html_content = """
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

        /* Custom select styles */
        .custom-select-wrapper {
            position: relative;
        }

        .custom-select {
            appearance: none;
            -webkit-appearance: none;
            background-color: #2A2A2A;
            border: 1px solid rgba(61, 205, 88, 0.3);
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
            padding-right: 2.5rem;
            font-size: 1rem;
            color: white;
            width: 100%;
            cursor: pointer;
        }

        .custom-select:focus {
            outline: none;
            border-color: #3DCD58;
        }

        .custom-select-arrow {
            position: absolute;
            top: 50%;
            right: 1rem;
            transform: translateY(-50%);
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #3DCD58;
            pointer-events: none;
        }

        .custom-select option {
            background-color: #1A1A1A;
            color: white;
            padding: 0.5rem;
        }
    </style>
</head>
<body class="min-h-screen hexagon-bg">
    <!-- Navigation Bar -->
    <nav class="bg-[#1A1A1A] border-b border-[#3DCD58]/20 p-4">
        <div class="container mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-4">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Schneider_Electric_2007.svg/2560px-Schneider_Electric_2007.svg.png" alt="Schneider Electric Logo" class="h-10">
                <span class="text-xl font-bold text-white">Procurement Analytics</span>
            </div>
            <div class="flex items-center space-x-6">
                <a href="#" class="text-gray-300 hover:text-[#3DCD58] transition-colors">Dashboard</a>
                <a href="#" class="text-gray-300 hover:text-[#3DCD58] transition-colors">History</a>
                <a href="#" class="text-gray-300 hover:text-[#3DCD58] transition-colors">Help</a>
            </div>
        </div>
    </nav>

    <div class="container mx-auto px-4 py-8">
        <!-- Hero Section -->
        <div class="text-center mb-12 animate__animated animate__fadeIn">
            <h1 class="text-4xl font-bold mb-4">Procurement Analysis Tool</h1>
            <p class="text-gray-400">Powered by India Effectiveness Team</p>
        </div>

        <!-- Main Content -->
        <div class="flex justify-center">
            <!-- Analysis Card -->
            <div class="se-card rounded-xl p-8 glow-effect w-full max-w-3xl">
                <h2 class="text-3xl font-bold mb-8 text-[#3DCD58]">New Analysis</h2>
                <form id="analysisForm" class="space-y-8">
                    <!-- Analysis Type Selection -->
                    <div class="relative">
                        <label class="block text-gray-400 text-lg font-medium mb-3">
                            Select Analysis Type
                        </label>
                        <div class="custom-select-wrapper">
                            <select id="analysisType" name="analysis_type" class="custom-select text-lg">
                                <option value="">Select an analysis...</option>
                                <option value="open_po">Open PO Analysis</option>
                                <option value="wwp">WWP Analysis</option>
                                <option value="rejected_part">Rejected Part Analysis</option>
                            </select>
                            <div class="custom-select-arrow"></div>
                        </div>
                    </div>

                    <!-- File Upload Instructions -->
                    <div id="fileUploadInstructions" class="hidden animate__animated animate__fadeIn">
                        <h3 class="text-xl font-medium text-[#3DCD58] mb-3">Required Files:</h3>
                        <ul id="fileList" class="list-disc pl-6 text-gray-400 space-y-2 text-lg"></ul>
                    </div>

                    <!-- File Upload Zone -->
                    <div id="fileUploadZone" class="hidden">
                        <div class="border-2 border-dashed border-[#3DCD58]/30 rounded-xl p-10 text-center 
                                    transition-all duration-300 hover:border-[#3DCD58]/60" 
                             id="dropZone">
                            <input type="file" id="fileInput" name="file" accept=".xlsx,.csv,.zip" class="hidden" multiple>
                            <label for="fileInput" class="cursor-pointer">
                                <div class="space-y-6">
                                    <div class="mx-auto h-20 w-20 text-[#3DCD58]/60">
                                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                                        </svg>
                                    </div>
                                    <div class="text-gray-300 text-xl">
                                        Drop your file(s) here or click to upload
                                    </div>
                                    <div class="text-gray-500 text-lg">
                                        Supported formats: .xlsx, .csv, .zip
                                    </div>
                                </div>
                            </label>
                        </div>
                    </div>

                    <!-- File Info -->
                    <div id="fileInfo" class="hidden animate__animated animate__fadeIn">
                        <h3 class="text-xl font-medium text-[#3DCD58] mb-3">Uploaded Files:</h3>
                        <ul id="uploadedFileList" class="list-disc pl-6 text-gray-400 space-y-2 text-lg"></ul>
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" 
                            class="w-full py-4 px-8 se-gradient rounded-lg text-white text-xl font-medium
                                   transform transition-all duration-300 hover:scale-105 disabled:opacity-50 
                                   disabled:hover:scale-100 focus:outline-none focus:ring-2 
                                   focus:ring-[#3DCD58]/50" 
                            disabled>
                        Run Analysis
                    </button>
                </form>
            </div>
        </div>

        <!-- Loading Indicator -->
        <div id="loadingIndicator" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div class="bg-[#2A2A2A] rounded-xl p-8 flex items-center space-x-4">
                <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#3DCD58]"></div>
                <span class="text-white">Processing your analysis...</span>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const select = document.getElementById('analysisType');
            const fileUploadInstructions = document.getElementById('fileUploadInstructions');
            const fileList = document.getElementById('fileList');
            const fileUploadZone = document.getElementById('fileUploadZone');
            const fileInput = document.getElementById('fileInput');
            const uploadedFileList = document.getElementById('uploadedFileList');
            const fileInfo = document.getElementById('fileInfo');
            const submitButton = document.querySelector('button[type="submit"]');
            
            select.addEventListener('change', function() {
                if (this.value) {
                    this.style.color = 'white';
                    fileUploadInstructions.classList.remove('hidden');
                    fileUploadZone.classList.remove('hidden');
                    fileList.innerHTML = '';
                    
                    if (this.value === 'open_po') {
                        fileList.innerHTML = `
                            <li>Open PO Report (.xlsx or .csv)</li>
                            <li>Workbench File (.xlsx or .csv)</li>
                        `;
                    } else if (this.value === 'wwp') {
                        fileList.innerHTML = `
                            <li>CAP Base Report (.xlsx or .csv)</li>
                        `;
                    } else if (this.value === 'rejected_part') {
                        fileList.innerHTML = `
                            <li>PDM ZIP File (.zip)</li>
                        `;
                    }
                } else {
                    this.style.color = 'rgba(255, 255, 255, 0.5)';
                    fileUploadInstructions.classList.add('hidden');
                    fileUploadZone.classList.add('hidden');
                }
                
                // Reset file input and hide file info
                fileInput.value = '';
                fileInfo.classList.add('hidden');
                uploadedFileList.innerHTML = '';
                submitButton.disabled = true;
            });

            fileInput.addEventListener('change', function(e) {
                const files = e.target.files;
                if (files.length > 0) {
                    fileInfo.classList.remove('hidden');
                    uploadedFileList.innerHTML = '';
                    for (let file of files) {
                        uploadedFileList.innerHTML += `<li>${file.name}</li>`;
                    }
                    submitButton.disabled = false;
                } else {
                    fileInfo.classList.add('hidden');
                    submitButton.disabled = true;
                }
            });

            // Prevent default drag behaviors
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                fileUploadZone.addEventListener(eventName, preventDefaults, false);
                document.body.addEventListener(eventName, preventDefaults, false);
            });

            // Highlight drop area when item is dragged over it
            ['dragenter', 'dragover'].forEach(eventName => {
                fileUploadZone.addEventListener(eventName, highlight, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                fileUploadZone.addEventListener(eventName, unhighlight, false);
            });

            // Handle dropped files
            fileUploadZone.addEventListener('drop', handleDrop, false);

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            function highlight(e) {
                fileUploadZone.classList.add('border-[#3DCD58]');
            }

            function unhighlight(e) {
                fileUploadZone.classList.remove('border-[#3DCD58]');
            }

            function handleDrop(e) {
                const dt = e.dataTransfer;
                const files = dt.files;
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
        });
    </script>
</body>
</html>
    """
    return html_content

def main():
    # Configure the page
    st.set_page_config(
        page_title="Procurement Analysis",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Hide Streamlit default elements
    hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stApp {
                margin-top: -80px;
            }
            /* Force the background color */
            .stApp > header {
                background-color: #1A1A1A;
            }
            .stApp {
                background-color: #1A1A1A;
            }
            section[data-testid="stSidebar"] {
                background-color: #1A1A1A;
            }
            /* Additional styles for file uploader */
            .stFileUploader > div > button {
                background-color: #3DCD58;
                color: white;
            }
            .stFileUploader > div {
                border-color: #3DCD58;
            }
        </style>
    """
    
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Add a container for better spacing
    with st.container():
        # Render the HTML template
        components.html(
            load_html_template(),
            height=800,
            scrolling=False
        )

        # Add file processing logic
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = []

        # Handle file uploads
        uploaded_files = st.file_uploader(
            "Upload your files",
            accept_multiple_files=True,
            type=['xlsx', 'csv', 'zip'],
            key='file_uploader'
        )

        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            
            # Add a process button
            if st.button('Process Files'):
                # Add your processing logic here
                with st.spinner('Processing files...'):
                    # Placeholder for your processing logic
                    st.success('Files processed successfully!')
                    
                    # You can add more processing results display here
                    st.write("Processing results:")
                    for file in uploaded_files:
                        st.write(f"Processed: {file.name}")

if __name__ == "__main__":
    main()
