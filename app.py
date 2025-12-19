import streamlit as st
import pandas as pd
import io
import zipfile
from pathlib import Path
import tempfile
import os
from typing import List, Dict, Any
import time
import logging

# Import custom modules
from modules.file_handler import ExcelFileHandler
from modules.converter import TemplateConverter
from modules.step2_processor import Step2Processor
from modules.step3_data_transfer import Step3DataTransfer
from modules.step4_duplicate_remover import Step4DuplicateRemover
from modules.exporter import FileExporter
from utils.validators import FileValidator

# Configure logging
logging.basicConfig(level=logging.INFO)

# Page configuration
st.set_page_config(
    page_title="Excel TSS Converter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_custom_css():
    """Load custom CSS styling for the app"""
    st.markdown("""
        <style>
        /* Import Roboto Font */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        /* Apply Roboto to all elements */
        * {
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif !important;
        }
        
        /* Global styles */
        .main {
            background-color: #f8f9fa;
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* Ensure all Streamlit elements use Roboto */
        .stSelectbox label, .stRadio label, .stButton button, .stFileUploader label,
        .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p, span, div {
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif !important;
        }
        
        /* Remove Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        header {visibility: hidden;}
        
        /* App title section */
        .app-header {
            text-align: center;
            padding: 0.375rem 0 0.25rem 0;
            margin: 0;
            background: transparent;
        }
        
        .app-title {
            font-size: 1.5rem;
            font-weight: 400;
            color: #333333;
            margin-bottom: 0.125rem;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.25rem;
        }
        
        .app-subtitle {
            font-size: 0.8rem;
            color: #666666;
            font-weight: 400;
            text-align: center;
        }
        
        /* Upload section styles */
        .upload-section {
            max-width: 800px;
            margin: 0 auto 0.375rem auto;
            background: transparent;
            border-radius: 0;
            overflow: visible;
            box-shadow: none;
            border: none;
            position: relative;
        }
        
        .upload-box-header {
            background: #ffffff;
            padding: 0.5rem 0.75rem;
            text-align: center;
            border: 2px dashed #d1d5db;
            border-radius: 8px;
            margin-bottom: 0.25rem;
        }
        
        .upload-box-header h3 {
            font-size: 1rem;
            font-weight: 500;
            color: #333333;
            margin-bottom: 0.125rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.25rem;
        }
        
        .upload-box-header p {
            font-size: 0.8rem;
            color: #666666;
            margin: 0;
        }
        
        .upload-box-body {
            background-color: transparent;
            padding: 0;
            text-align: left;
        }
        
        .drag-drop-area {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 2rem;
            border: none;
            border-radius: 8px;
            background: #f8f9fa;
        }
        
        .drag-drop-content {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .drag-drop-icon {
            font-size: 2.5rem;
            color: #6c757d;
        }
        
        .drag-drop-text h4 {
            margin: 0;
            font-size: 1.1rem;
            font-weight: 400;
            color: #333333;
        }
        
        .drag-drop-text p {
            margin: 0;
            font-size: 0.95rem;
            color: #6c757d;
        }
        
        .browse-button {
            background: #ffffff;
            border: 1px solid #ced4da;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            font-size: 0.9rem;
            color: #495057;
            cursor: pointer;
            white-space: nowrap;
            font-weight: 400;
        }
        
        .browse-button:hover {
            background: #f8f9fa;
            border-color: #adb5bd;
        }
        
        /* Style file uploader to match design */
        
        .stFileUploader > div {
            border: 2px dashed #d1d5db !important;
            background: #ffffff !important;
            border-radius: 8px !important;
            padding: 0.5rem 0.75rem !important;
            margin: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            box-sizing: border-box !important;
            width: 100% !important;
        }
        
        .stFileUploader label {
            display: none !important;
        }
        
        .stFileUploader > div > div {
            border: none !important;
            background: transparent !important;
            margin: 0 !important;
        }
        
        .stFileUploader > div > div > div {
            border: none !important;
            background: transparent !important;
            text-align: left !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            margin: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
            overflow: visible !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }
        
        /* Constrain all content within exact bounds */
        .stFileUploader section {
            border: none !important;
            background: transparent !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }
        
        /* Force button to respect container bounds */
        .stFileUploader button {
            margin: 0 !important;
            flex-shrink: 1 !important;
            max-width: 120px !important;
            width: auto !important;
            min-width: 0 !important;
            overflow: hidden !important;
            white-space: nowrap !important;
            text-overflow: ellipsis !important;
        }
        
        /* Force all file uploader content to stay within bounds */
        .stFileUploader * {
            max-width: 100% !important;
            box-sizing: border-box !important;
        }
        
        /* Additional constraint on the button container */
        .stFileUploader > div > div > div > div {
            max-width: 100% !important;
            overflow: hidden !important;
        }
        
        
        /* Align upload area with header */
        .upload-box-body {
            background-color: #ffffff;
            padding: 0 2rem 2rem 2rem;
            text-align: left;
        }
        
        /* Ensure file uploader fits within container bounds */
        .stFileUploader {
            border: none !important;
            background: transparent !important;
            margin: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }
        
        /* Create wrapper for file uploader */
        .file-uploader-wrapper {
            width: 100%;
            max-width: 100%;
            overflow: hidden;
            position: relative;
        }
        
        /* Ensure file uploader matches header width exactly */
        .stFileUploader {
            border: none !important;
            background: transparent !important;
            margin: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }
        
        /* Hide file information section */
        .file-info {
            display: none !important;
        }
        
        /* Hide processing options section */
        .stRadio {
            display: none !important;
        }
        
        /* Hide all markdown sections after upload */
        .uploaded-file-info {
            display: none !important;
        }
        
        /* Style the Start Conversion button */
        .conversion-button {
            text-align: center;
            margin: 0.25rem 0;
        }
        
        .stButton > button {
            background-color: #007bff !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.5rem 1.5rem !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            transition: background-color 0.2s !important;
        }
        
        .stButton > button:hover {
            background-color: #0056b3 !important;
        }
        
        /* Hide all info boxes and processing sections */
        .stInfo, .stSuccess, .stWarning, .stError {
            display: none !important;
        }
        
        
        /* Progress bar styles */
        .stProgress > div > div > div > div {
            background-color: #3b82f6;
        }
        
        /* Success/Error message styles */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Custom file info display */
        .file-info {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            padding: 1.5rem;
            margin: 2rem 0;
        }
        
        .file-info h4 {
            color: #1e3a8a;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }
        
        .file-info p {
            color: #64748b;
            margin: 0.5rem 0;
            font-size: 1rem;
            line-height: 1.5;
        }
        
        /* Results section */
        .results-section {
            margin-top: 2rem;
            padding: 1.5rem;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            background-color: #FAFAFA;
        }
        
        .download-item {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            padding: 1rem;
            margin: 0.5rem 0;
            display: flex;
            justify-content: between;
            align-items: center;
        }
        
        </style>
    """, unsafe_allow_html=True)


def display_header():
    """Display the application header"""
    st.markdown("""
        <div class="app-header">
            <h1 class="app-title">📊 CPC Internal TSS Converter</h1>
            <p class="app-subtitle">Convert CPC Internal TSS to Standard Internal TSS</p>
        </div>
    """, unsafe_allow_html=True)

def display_upload_section():
    """Display the file upload interface"""
    st.markdown("""
        <div class="upload-section">
            <div class="upload-box-header">
                <h3>📁 Upload Excel File</h3>
                <p>Select .xlsx file to convert</p>
            </div>
            <div class="upload-box-body">
                <div class="file-uploader-wrapper">
    """, unsafe_allow_html=True)
    
    # File uploader with custom styling
    uploaded_file = st.file_uploader(
        "Choose Excel file",
        type=['xlsx', 'xls'],
        help="Upload your Excel file (max 200MB)",
        label_visibility="collapsed"
    )
    
    st.markdown("""
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    return uploaded_file

def display_file_info(file_info: Dict[str, Any]):
    """Display information about the uploaded file"""
    st.markdown(f"""
        <div class="file-info">
            <h4>📄 File Information</h4>
            <p><strong>Filename:</strong> {file_info['filename']}</p>
            <p><strong>File size:</strong> {file_info['size']}</p>
            <p><strong>Number of sheets:</strong> {file_info['sheet_count']}</p>
            <p><strong>Non-empty sheets:</strong> {file_info['non_empty_sheets']}</p>
        </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Load custom CSS
    load_custom_css()
    
    # Display app header
    display_header()
    
    # Initialize session state
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = []
    if 'step2_files' not in st.session_state:
        st.session_state.step2_files = []
    if 'step3_files' not in st.session_state:
        st.session_state.step3_files = []
    if 'step4_files' not in st.session_state:
        st.session_state.step4_files = []
    
    # Display upload section
    uploaded_file = display_upload_section()
    
    if uploaded_file is not None:
        # Show Start Conversion button
        st.markdown('<div class="conversion-button">', unsafe_allow_html=True)
        start_conversion = st.button("🔄 Start Conversion", key="start_conversion_btn", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if start_conversion:
            try:
                # Initialize components
                file_handler = ExcelFileHandler()
                validator = FileValidator()
                converter = TemplateConverter()
                step2_processor = Step2Processor()
                step3_processor = Step3DataTransfer()
                step4_processor = Step4DuplicateRemover()
                exporter = FileExporter()
                
                # Validate file
                with st.spinner("Validating file..."):
                    is_valid, validation_message = validator.validate_excel_file(uploaded_file)
                
                if not is_valid:
                    st.error(f"❌ File validation failed: {validation_message}")
                    return
                
                # Process file
                with st.spinner("Reading Excel file..."):
                    file_info = file_handler.get_file_info(uploaded_file)
                    sheets_data = file_handler.read_excel_sheets(uploaded_file)
                
                # Show non-empty sheets
                non_empty_sheets = [name for name, df in sheets_data.items() if not df.empty]
                
                if not non_empty_sheets:
                    st.warning("⚠️ No non-empty sheets found in the uploaded file.")
                    return
                
                # Start processing
                with st.spinner("Processing files..."):
                    # Initialize components
                    progress_bar = st.progress(0)
                    
                    # Step 1: Create templates first
                    converter = TemplateConverter()
                    processed_files = []
                    for sheet_name in non_empty_sheets:
                        template_file = converter.create_template_for_sheet(sheet_name, uploaded_file.name)
                        if template_file:
                            base_name = Path(uploaded_file.name).stem
                            processed_files.append({
                                'sheet_name': sheet_name,
                                'filename': f"{base_name} - {sheet_name} - Step1.xlsx",
                                'file_path': template_file
                            })
                    progress_bar.progress(0.25)
                    
                    # Process with complete pipeline
                    step2_results = step2_processor.process_multiple_sheets_to_step2(uploaded_file, processed_files)
                    progress_bar.progress(0.5)
                    
                    if step2_results['step2_files']:
                        step3_results = step3_processor.process_multiple_sheets_to_step3(uploaded_file, step2_results['step2_files'])
                        progress_bar.progress(0.75)
                        
                        if step3_results['step3_files']:
                            step4_results = step4_processor.process_multiple_sheets_to_step4(step3_results['step3_files'])
                            progress_bar.progress(1.0)
                            
                            if step4_results['step4_files']:
                                # Create download
                                zip_buffer = exporter.create_zip_download(step4_results['step4_files'])
                                
                                st.success("✅ Conversion completed successfully!")
                                st.download_button(
                                    label="📦 Download Converted Files",
                                    data=zip_buffer,
                                    file_name=f"{Path(uploaded_file.name).stem}_TSS_Converted.zip",
                                    mime="application/zip"
                                )
            except Exception as process_error:
                st.error(f"❌ Error during processing: {str(process_error)}")
                logging.error(f"Processing error: {str(process_error)}")
    

if __name__ == "__main__":
    main()