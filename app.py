import streamlit as st
from pathlib import Path
from typing import Any
import logging

# Import custom modules
from modules.file_handler import ExcelFileHandler
from modules.converter import TemplateConverter
from modules.step2_processor import Step2Processor
from modules.step3_data_transfer import Step3DataTransfer
from modules.step4_duplicate_remover import Step4DuplicateRemover
from modules.exporter import FileExporter
from utils.validators import FileValidator

# Import TSS UI Kit
from modules.tss_ui_kit import TSSUIKit, create_config, get_step_config

# Configure logging
logging.basicConfig(level=logging.INFO)

# Page configuration
st.set_page_config(
    page_title="Excel TSS Converter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize TSS UI Kit
@st.cache_resource
def initialize_ui_kit():
    """Initialize and cache the TSS UI Kit instance"""
    config = create_config({
        "app_title": "CPC Internal TSS Converter",
        "page_title": "CPC Internal TSS Converter",
        "max_file_size_mb": 100,
        "layout": "wide",
        "initial_sidebar_state": "collapsed"
    })
    ui = TSSUIKit(config.export_config())
    return ui, config

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
        
        /* Hide footer completely */
        footer, .stApp > footer, [data-testid="stFooter"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }
        
        /* App title section */
        .app-header {
            text-align: center;
            padding: 0.375rem 0 0.25rem 0;
            margin: 0;
            background: transparent;
        }
        
        .app-title {
            font-size: 2.5rem;
            font-weight: 400;
            color: #333333;
            margin-bottom: 0.5rem;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.25rem;
        }
        
        .app-subtitle {
            font-size: 1.1rem;
            color: #666666;
            font-weight: 400;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Upload section styles - New Design */
        .upload-section {
            max-width: 900px;
            margin: 0 auto 2rem auto;
            background: transparent;
        }
        
        .upload-header {
            background: #ffffff;
            padding: 0.75rem;
            text-align: center;
            border: 2px dashed #d1d5db;
            border-radius: 8px 8px 0 0;
            border-bottom: 1px solid #d1d5db;
        }
        
        .upload-header h3 {
            font-size: 1.2rem;
            font-weight: 500;
            color: #333333;
            margin-bottom: 0.5rem;
        }
        
        .upload-header p {
            font-size: 0.9rem;
            color: #666666;
            margin: 0;
        }
        
        
        /* Streamlit file uploader - centered below text */
        
        .stFileUploader {
            border: none !important;
            background: transparent !important;
            margin: 0 !important;
            position: static !important;
            width: auto !important;
            max-width: none !important;
            text-align: center !important;
        }
        
        .stFileUploader > div {
            border: none !important;
            background: transparent !important;
            border-radius: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            width: auto !important;
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
            text-align: center !important;
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 0 !important;
            margin: 0 !important;
            width: 100% !important;
            max-width: none !important;
            overflow: visible !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }
        
        /* Override Streamlit file uploader completely */
        .stFileUploader {
            border: none !important;
            background: transparent !important;
            max-width: 900px !important;
            margin: 0 auto !important;
        }
        
        .stFileUploader > div {
            border: 2px dashed #d1d5db !important;
            border-top: none !important;
            background-color: #f8f9fa !important;
            border-radius: 0 0 8px 8px !important;
            padding: 1.5rem 3rem !important;
            margin: 0 !important;
        }
        
        .stFileUploader > div > div {
            background-color: #f8f9fa !important;
        }
        
        .stFileUploader section {
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            background-color: #f8f9fa !important;
            border: none !important;
            padding: 1rem 0.25rem 1rem 1rem !important;
        }
        
        /* Style the drag drop area like the reference */
        .stFileUploader section > div:first-child {
            display: flex !important;
            align-items: center !important;
            gap: 1rem !important;
        }
        
        /* Remove the extra cloud icon */
        .stFileUploader section::before {
            display: none !important;
        }
        
        /* Show only the button and position it to the right */
        .stFileUploader button {
            display: block !important;
            margin: 0 0 0 auto !important;
            margin-right: 0.25rem !important;
            background: #ffffff !important;
            border: 1px solid #ced4da !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 6px !important;
            font-size: 0.9rem !important;
            color: #495057 !important;
            cursor: pointer !important;
            white-space: nowrap !important;
            font-weight: 400 !important;
            position: relative !important;
            right: 0 !important;
        }
        
        .stFileUploader button:hover {
            background: #f8f9fa !important;
            border-color: #adb5bd !important;
        }
        
        /* Additional hiding for Streamlit elements */
        .stFileUploader [data-testid="stFileUploader"] > div {
            display: none !important;
        }
        
        .stFileUploader [data-testid="stFileUploader"] button {
            display: block !important;
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
        
        
        
        /* Main upload area - New Design */
        .main-upload-area {
            background: #f8f9fa;
            border: none;
            border-radius: 0 0 8px 8px;
            padding: 1rem 2rem;
            text-align: center;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .upload-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            max-width: 100%;
            position: relative;
            gap: 1rem;
        }
        
        .cloud-icon {
            font-size: 2.5rem;
            color: #6c757d;
            margin-bottom: 0.5rem;
        }
        
        .upload-text {
            text-align: center;
        }
        
        .upload-text h4 {
            margin: 0 0 0.5rem 0;
            font-size: 1.1rem;
            font-weight: 400;
            color: #333333;
        }
        
        .upload-text p {
            margin: 0;
            font-size: 0.9rem;
            color: #6c757d;
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
        
        
        /* Hide all info boxes and processing sections */
        .stInfo, .stSuccess, .stWarning, .stError {
            display: none !important;
        }
        
        
        /* Progress bar styles */
        .stProgress > div > div > div > div {
            background-color: #2563eb;
        }
        
        /* Success/Error message styles */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Custom file info display - match upload box width */
        .file-info {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            padding: 1.5rem;
            margin: 2rem auto;
            width: 70%;
            max-width: 800px;
            min-width: 350px;
            box-sizing: border-box;
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


def display_header(ui: TSSUIKit):
    """Display the application header using TSS UI Kit"""
    ui.render_app_header(
        title="CPC Internal TSS Converter",
        subtitle="Convert CPC Internal TSS to Standard Internal TSS",
        icon="📊",
        compact=True,
        show_line=True
    )

def display_upload_section(ui: TSSUIKit):
    """Display the file upload interface with TSS UI Kit styling"""
    # Use TSS UI Kit header but keep original Streamlit file uploader for compatibility
    st.markdown("""
        <div class="upload-area-compact">
            <h4 class="upload-title">📁 Upload File</h4>
            <p class="upload-subtitle">Select Excel file to process</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Use original Streamlit file uploader for full compatibility
    uploaded_file = st.file_uploader(
        "Select file",
        type=['xlsx', 'xls'],
        help="Upload your Excel file (max 100MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Show file info using TSS UI Kit styling
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        ui.render_info_message(f"File uploaded: {uploaded_file.name} ({file_size_mb:.1f}MB)")
    
    return uploaded_file


def main():
    """Main application function"""
    # Initialize TSS UI Kit
    ui, _ = initialize_ui_kit()
    
    # Apply TSS UI Kit styling
    ui.inject_custom_css()
    
    # Display app header
    display_header(ui)
    
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
    uploaded_file = display_upload_section(ui)
    
    if uploaded_file is not None:
        # Use columns to center button - simplest working solution
        col1, col2, col3 = st.columns([2, 1, 2])  
        with col2:
            start_conversion = st.button("🔄 Start Conversion", type="primary", 
                                       key="start_conversion_btn", use_container_width=True)
        
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
                    ui.render_error_message(f"File validation failed: {validation_message}")
                    return
                
                # Process file
                with st.spinner("Reading Excel file..."):
                    sheets_data = file_handler.read_excel_sheets(uploaded_file)
                
                # Show non-empty sheets
                non_empty_sheets = [name for name, df in sheets_data.items() if not df.empty]
                
                if not non_empty_sheets:
                    ui.render_warning_message("No non-empty sheets found in the uploaded file.")
                    return
                
                # Start processing with single progress tracker
                with st.spinner("Processing files..."):
                    # Create single progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Create templates first
                    status_text.info("⏳ Step 1: Creating template files...")
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
                    status_text.success("✅ Step 1: Template creation completed")
                    
                    # Step 2: Data Processing
                    status_text.info("⏳ Step 2: Processing data...")
                    step2_results = step2_processor.process_multiple_sheets_to_step2(uploaded_file, processed_files)
                    progress_bar.progress(0.5)
                    status_text.success("✅ Step 2: Data processing completed")
                    
                    if step2_results['step2_files']:
                        # Step 3: Data Transfer
                        status_text.info("⏳ Step 3: Transferring data...")
                        step3_results = step3_processor.process_multiple_sheets_to_step3(uploaded_file, step2_results['step2_files'])
                        progress_bar.progress(0.75)
                        status_text.success("✅ Step 3: Data transfer completed")
                        
                        if step3_results['step3_files']:
                            # Step 4: Duplicate Removal
                            status_text.info("⏳ Step 4: Removing duplicates...")
                            step4_results = step4_processor.process_multiple_sheets_to_step4(step3_results['step3_files'])
                            progress_bar.progress(1.0)
                            status_text.success("✅ Step 4: Duplicate removal completed")
                            
                            if step4_results['step4_files']:
                                # Create download using TSS UI Kit
                                zip_buffer = exporter.create_zip_download(step4_results['step4_files'])
                                
                                # Save to temporary file for TSS UI Kit download
                                import tempfile
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                                    tmp_file.write(zip_buffer)
                                    temp_file_path = tmp_file.name
                                
                                ui.render_success_message("Conversion completed successfully!")
                                
                                # Use TSS UI Kit download section
                                ui.render_download_section(
                                    file_path=temp_file_path,
                                    original_filename=uploaded_file.name,
                                    custom_filename=f"{Path(uploaded_file.name).stem}_TSS_Converted.zip"
                                )
            except Exception as process_error:
                ui.render_error_message(f"Error during processing: {str(process_error)}")
                logging.error(f"Processing error: {str(process_error)}")
    

if __name__ == "__main__":
    main()