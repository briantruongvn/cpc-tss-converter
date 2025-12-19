# Claude Code Guide - Excel Converter Web App

## Project Objective
Create a Python web application to convert Excel files (potentially multiple sheets) to a desired format, deployed on Streamlit.

## Technical Requirements

### Technology Stack
- **Framework**: Streamlit
- **Language**: Python 3.8+
- **Excel Processing Libraries**: 
  - `pandas` - read/write Excel
  - `openpyxl` - xlsx format support
  - `xlrd` - xls format support (if needed)

### Core Features
1. **Upload Interface**
   - Allow Excel file upload (.xlsx, .xls)
   - Display file information (name, size, number of sheets)
   - Preview sheet contents

2. **Processing Module**
   - Read all sheets in Excel file
   - Conversion logic processing module (to be defined later)
   - Input data validation

3. **Output Module**
   - Export Excel file in new format
   - Download button
   - Preview results before download

4. **UI/UX Requirements**
   - Simple, clear interface
   - Display progress bar during processing
   - Error handling with user-friendly messages
   - Responsive design

## UI Design

### Tham khảo từ Ngoc Son TSS Converter App

#### Layout Structure
```
┌─────────────────────────────────────────────────┐
│  [Icon] Title                                   │
│  Subtitle/Description                           │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  📁 Upload Excel File                     │ │
│  │  Select .xlsx file to convert             │ │
│  ├───────────────────────────────────────────┤ │
│  │                                           │ │
│  │  ☁️  Drag and drop file here             │ │
│  │     Limit 200MB per file • XLSX          │ │
│  │                        [Browse files]    │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### Color Scheme
- **Background**: Trắng sạch (#FFFFFF)
- **Primary Text**: Đen (#000000) cho title
- **Secondary Text**: Xám (#808080) cho subtitle và description
- **Border**: Xám nhạt với border-dashed cho upload area
- **Upload Area Background**: Xám rất nhạt (#F7F9FB hoặc tương tự)
- **Button**: Trắng với border xám

#### Typography
- **Main Title**: 
  - Font: Sans-serif (system default hoặc Inter/Roboto)
  - Size: ~40-48px
  - Weight: Bold
  - Color: Black

- **Subtitle**: 
  - Font: Sans-serif
  - Size: ~18-20px
  - Weight: Regular
  - Color: Gray (#808080)

- **Section Headers**: 
  - Font: Sans-serif
  - Size: ~20-24px
  - Weight: 600
  - Color: Dark gray (#333333)

- **Body Text**: 
  - Font: Sans-serif
  - Size: ~14-16px
  - Weight: Regular
  - Color: Gray (#666666)

#### Components Style

**Upload Box**:
- Border: 2px dashed #E0E0E0
- Border-radius: 8-12px
- Background: #F7F9FB
- Padding: 40px
- Center-aligned content

**Icon**: 
- Use emoji or icon library (📊, 📁, ☁️)
- Size: 24-32px
- Color: Matching with text

**Browse Button**:
- Background: White
- Border: 1px solid #D0D0D0
- Border-radius: 6px
- Padding: 8px 16px
- Hover effect: Slight shadow

### Custom CSS Implementation

```python
# Custom CSS to create similar interface
st.markdown("""
    <style>
    /* Import font if needed */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global styles */
    .main {
        background-color: #FFFFFF;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Header styles */
    .app-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .app-subtitle {
        font-size: 1.1rem;
        color: #808080;
        font-weight: 400;
    }
    
    /* Upload section */
    .upload-section {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 0 2rem;
    }
    
    .upload-box-header {
        background-color: #FFFFFF;
        border: 2px dashed #E0E0E0;
        border-bottom: none;
        border-radius: 12px 12px 0 0;
        padding: 1.5rem;
        text-align: center;
    }
    
    .upload-box-header h3 {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333333;
        margin-bottom: 0.5rem;
    }
    
    .upload-box-header p {
        font-size: 0.95rem;
        color: #666666;
        margin: 0;
    }
    
    .upload-box-body {
        background-color: #F7F9FB;
        border: 2px dashed #E0E0E0;
        border-top: 1px solid #E0E0E0;
        border-radius: 0 0 12px 12px;
        padding: 3rem 2rem;
        text-align: center;
    }
    
    /* Streamlit file uploader override */
    .stFileUploader {
        border: none !important;
        background: transparent !important;
    }
    
    .stFileUploader > div {
        border: none !important;
        padding: 0 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Button styles */
    .stButton > button {
        background-color: #FFFFFF;
        border: 1px solid #D0D0D0;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        color: #333333;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-color: #B0B0B0;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 8px;
        padding: 1rem;
    }
    
    </style>
""", unsafe_allow_html=True)
```

## Project Structure

```
excel-converter/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── modules/
│   ├── __init__.py
│   ├── file_handler.py        # Upload & read Excel
│   ├── converter.py           # Conversion logic (placeholder)
│   └── exporter.py            # Export Excel
├── utils/
│   ├── __init__.py
│   └── validators.py          # Validation functions
├── assets/                    # Optional: images, icons
│   └── icon.png              # App icon
└── README.md
```

## Implementation Steps

### Phase 1: Basic Setup and UI
1. Create Streamlit app with custom CSS styling
2. Implement header with icon and title
3. Create upload interface with styling similar to reference app
4. Configure Streamlit settings (config.toml)

### Phase 2: File Handling
1. Implement file upload with validation
2. Read Excel file with pandas
3. Display file information (name, size, number of sheets)
4. Preview sheet contents with formatting

### Phase 3: Processing Framework
1. Create converter module with flexible structure
2. Implement placeholder functions for conversion logic
3. Add validation layer
4. Progress indicator during processing

### Phase 4: Export & Download
1. Create export module
2. Implement download functionality with custom button
3. Add preview before download
4. Success message with download link

### Phase 5: Polish & Testing
1. Refine UI/UX details
2. Add comprehensive error handling
3. Testing with sample Excel files
4. Optimize performance for large files
5. Mobile responsive check

## Dependencies (requirements.txt)

```txt
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
xlrd>=2.0.0
Pillow>=10.0.0  # For icon handling if needed
```

## Configuration (.streamlit/config.toml)

```toml
[theme]
primaryColor="#000000"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F7F9FB"
textColor="#333333"
font="sans serif"

[server]
maxUploadSize=200
enableXsrfProtection=true
```

## App Structure Example (app.py outline)

```python
import streamlit as st
import pandas as pd
from modules import file_handler, converter, exporter

# Page config
st.set_page_config(
    page_title="Excel Converter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
load_custom_css()

# Header
display_header()

# Upload Section
uploaded_file = display_upload_section()

# Processing
if uploaded_file:
    # Validate file
    # Read Excel
    # Display preview
    # Convert button
    # Show results
    # Download button
```

## Deployment Notes (Streamlit Cloud)
- File size limit: 200MB (matches UI message)
- Memory: 1GB RAM
- Python version: 3.8+
- Environment variables: config in Streamlit dashboard
- Custom domain: can be set up if needed

## Next Steps
1. ✅ UI/UX design specifications completed
2. ⏳ Define specific conversion logic
3. ⏳ Define input/output Excel format structure
4. ⏳ Implementation with Claude Code

## Notes for Claude Code
- Use custom CSS extensively to match reference design
- Center-align main elements
- Maintain clean, minimalist aesthetic
- Focus on typography hierarchy
- Use subtle colors and spacing
- Implement proper error states
- Add loading states with spinner or progress bar
- Test thoroughly with different screen sizes