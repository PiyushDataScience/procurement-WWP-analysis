import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from analysis_logic import open_po_analysis  # Import your analysis logic

# Set up the page configuration for Streamlit
st.set_page_config(page_title="Procurement Analysis Tool", page_icon="📊")

# HTML content for the frontend
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procurement Analysis - Schneider Electric</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet">
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

        .custom-select {
            background-color: #2A2A2A;
            color: white;
            border: 1px solid rgba(61, 205, 88, 0.3);
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
            width: 100%;
            cursor: pointer;
        }
        
        .upload-area {
            border: 2px dashed #3DCD58;
            padding: 20px;
            text-align: center;
            transition: border-color 0.3s;
        }

        .upload-area:hover {
            border-color: #3DCD58;
        }
    </style>
</head>
<body class="min-h-screen">
    <!-- Navigation Bar -->
    <nav class="bg-[#1A1A1A] border-b border-[#3DCD58]/20 p-4">
        <div class="container mx-auto flex justify-between items-center">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Schneider_Electric_2007.svg/2560px-Schneider_Electric_2007.svg.png" alt="Schneider Electric Logo" class="h-10">
            <span class="text-xl font-bold text-white">Procurement Analytics</span>
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
            <div class="se-card rounded-xl p-8 glow-effect w-full max-w-3xl">
                <h2 class="text-3xl font-bold mb-8 text-[#3DCD58]">New Analysis</h2>
                <form id="analysisForm" class="space-y-8">

                    <!-- Single Analysis Type Selection -->
                    <div class="relative">
                        <label class="block text-gray-400 text-lg font-medium mb-3">Select Analysis Type</label>
                        <select id="analysisType" name="analysis_type" class="custom-select text-lg">
                            <option value="">Select an analysis...</option>
                            <option value="open_po">Open PO Analysis</option>
                            <option value="wwp">WWP Analysis</option>
                            <option value="rejected_part">Rejected Part Analysis</option>
                        </select>
                    </div>

                    <!-- File Upload Zone -->
                    <div class="upload-area">
                        <input type="file" id="fileInput" name="file" accept=".xlsx,.csv,.zip" class="hidden" multiple>
                        <label for="fileInput" class="cursor-pointer">
                            <p>Drop your file(s) here or click to upload</p>
                            <p class="text-gray-500">Supported formats: .xlsx, .csv, .zip</p>
                        </label>
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" class="w-full py-4 px-8 se-gradient rounded-lg text-white text-xl font-medium hover:scale-105 focus:outline-none" disabled>
                        Run Analysis
                    </button>
                </form>
            </div>
        </div>
    </div>

    <script>
        // JavaScript interactivity for file input
        document.getElementById('analysisType').addEventListener('change', function() {
            const fileInput = document.getElementById('fileInput');
            const submitButton = document.querySelector('button[type="submit"]');
            if (this.value) {
                fileInput.classList.remove('hidden');
                submitButton.disabled = false; // Enable the button
            } else {
                fileInput.classList.add('hidden');
                submitButton.disabled = true; // Disable the button
            }
        });
    </script>
</body>
</html>
"""

# Render the HTML frontend
components.html(html_content, height=800)
