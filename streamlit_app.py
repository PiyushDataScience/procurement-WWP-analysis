import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

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
            /* Your existing styles here */
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
        </style>
    </head>
    <body class="min-h-screen">
        <div id="content">
            <!-- Analysis Type Selection -->
            <div class="container mx-auto px-4 py-8">
                <div class="se-card rounded-xl p-8 glow-effect w-full max-w-3xl mx-auto">
                    <h2 class="text-3xl font-bold mb-8 text-[#3DCD58]">Open PO Analysis</h2>
                    <form id="uploadForm">
                        <div class="space-y-8">
                            <!-- File Upload Section -->
                            <div class="border-2 border-dashed border-[#3DCD58]/30 rounded-xl p-10 text-center">
                                <div class="space-y-6">
                                    <div class="mx-auto h-20 w-20 text-[#3DCD58]/60">
                                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                                        </svg>
                                    </div>
                                    <div class="text-gray-300 text-xl">
                                        Upload required files:
                                    </div>
                                    <div class="text-gray-500 text-lg">
                                        1. Open PO Report (.xlsx, .csv)<br>
                                        2. Workbench File (.xlsx, .csv)
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <script>
            // Handle communication with Streamlit
            function sendToStreamlit(data) {
                window.parent.postMessage({type: 'streamlit', data: data}, '*');
            }
        </script>
    </body>
    </html>
    """
    return html_content

def main():
    st.set_page_config(
        page_title="Procurement Analysis",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Inject custom CSS to hide Streamlit elements
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stApp {
                margin-top: -80px;
            }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
