# TSS UI Kit - Professional Streamlit Components

A comprehensive, reusable UI component library extracted from the TSS Converter project. Build professional data processing web applications with consistent, beautiful components.

## ✨ Features

- **Professional UI Components**: Headers, file upload, progress tracking, statistics display
- **Multiple Themes**: Default, dark, minimal, and corporate themes
- **Configurable Settings**: Flexible configuration system for all components
- **File Processing**: Built-in validation, size limits, and type checking
- **Progress Tracking**: Real-time progress indicators with step management
- **Error Handling**: Comprehensive error messages with optional details
- **Responsive Design**: Mobile-friendly layouts and responsive styling
- **Streamlit Branding Removal**: Clean professional appearance

## 🚀 Quick Start

```python
import streamlit as st
from tss_ui_kit import quick_setup

# One-line setup with theme
ui = quick_setup("My Data App", theme="default")

# Build your UI
ui.render_app_header("Data Processor", "Upload and process your files")
file_data = ui.render_file_upload_area()

if file_data:
    ui.render_success_message("File uploaded successfully!")
```

## 📦 Installation

Simply copy the `tss_ui_kit` folder to your project:

```
your_project/
├── tss_ui_kit/
│   ├── __init__.py
│   ├── components.py
│   ├── styles.py
│   └── config.py
└── your_app.py
```

### Requirements

- `streamlit >= 1.28.0`
- Python 3.8+

## 🎨 Themes

Choose from 4 built-in themes:

### Default Theme
Clean blue theme with professional styling
```python
ui = quick_setup("My App", theme="default")
```

### Dark Theme  
Dark theme for low-light environments
```python
ui = quick_setup("My App", theme="dark")
```

### Minimal Theme
Clean minimal theme with essential styling only
```python
ui = quick_setup("My App", theme="minimal")
```

### Corporate Theme
Professional corporate styling
```python
ui = quick_setup("My App", theme="corporate")
```

## 🧩 Components

### App Header
```python
ui.render_app_header(
    title="My Application",
    subtitle="Process your data efficiently", 
    icon="⚡",
    compact=False
)
```

### File Upload
```python
file_data = ui.render_file_upload_area(
    accepted_types=["xlsx", "csv", "json"],
    help_text="Upload files up to 50MB"
)

if file_data:
    file_bytes, filename = file_data
    # Process file...
```

### Progress Tracking
```python
step_status = {
    "step1": "completed",
    "step2": "running", 
    "step3": "pending"
}

ui.render_progress_section(
    current_step=2,
    step_status=step_status,
    step_config=get_step_config()
)
```

### Messages
```python
ui.render_success_message("Operation completed!")
ui.render_error_message("Error occurred", details="Connection timeout")
ui.render_warning_message("Please check your input")
ui.render_info_message("Processing will begin shortly")
```

### Download Section
```python
ui.render_download_section(
    file_path="output.xlsx",
    original_filename="input.xlsx",
    processing_stats={"rows": 1000, "time": 15.5}
)
```

### Statistics Display
```python
stats = {
    "initial_rows": 10000,
    "final_rows": 9500,
    "processing_time": 23.4
}
ui.render_processing_stats(stats)
```

## ⚙️ Advanced Configuration

### Custom Configuration
```python
from tss_ui_kit import TSSUIKit, create_config

config = create_config({
    "app_title": "Advanced App",
    "max_file_size_mb": 100,
    "theme": {"primary_color": "#1f2937"},
    "show_error_details": True
})

st.set_page_config(**config.get_streamlit_config())
ui = TSSUIKit(config.export_config())
ui.inject_custom_css()
```

### Custom Step Configuration
```python
from tss_ui_kit import create_custom_step_config

custom_steps = [
    {"name": "Upload", "description": "File upload", "icon": "📤"},
    {"name": "Process", "description": "Data processing", "icon": "⚙️"},
    {"name": "Export", "description": "Generate output", "icon": "📥"}
]

step_config = create_custom_step_config(custom_steps)
```

### Theme Customization
```python
from tss_ui_kit import get_custom_css, get_dark_theme_css

# Apply custom styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Or use dark theme
st.markdown(get_dark_theme_css(), unsafe_allow_html=True)
```

## 📚 Complete Example

```python
import streamlit as st
from tss_ui_kit import TSSUIKit, create_config, get_step_config

# Configure app
config = create_config({
    "app_title": "Data Processor",
    "max_file_size_mb": 50
})

st.set_page_config(**config.get_streamlit_config())

# Create UI Kit
ui = TSSUIKit(config.export_config())
ui.inject_custom_css()

# Build interface
ui.render_app_header(
    title="Professional Data Processor",
    subtitle="Upload, process, and download your Excel files"
)

# File upload
file_data = ui.render_file_upload_area(["xlsx"])

if file_data:
    file_bytes, filename = file_data
    
    # Process button
    if st.button("🚀 Start Processing", type="primary"):
        # Simulate processing
        step_status = {"step1": "running", "step2": "pending"}
        ui.render_progress_section(1, step_status, get_step_config())
        
        # Show results
        ui.render_success_message("Processing completed!")
        
        # Download section
        ui.render_download_section(
            file_path="processed_file.xlsx",
            original_filename=filename
        )

# Help sidebar
help_content = {
    "🚀 Getting Started": "Upload an Excel file to begin processing",
    "📁 Supported Files": "Excel (.xlsx) files up to 50MB",
    "❓ Support": "Contact support for assistance"
}
ui.render_help_section(help_content)

# Footer
ui.render_footer("Data Processor", "1.0")
```

## 🎯 Demo Application

Run the included demo to explore all features:

```bash
streamlit run tss_ui_kit_demo.py
```

The demo includes:
- Quick setup examples
- Full configuration demos  
- Component gallery
- Theme comparisons
- Interactive examples

## 🔧 Configuration Options

### File Upload Settings
- `max_file_size_mb`: Maximum upload size (default: 50MB)
- `allowed_file_types`: Accepted file extensions
- `upload_directory`: Directory for temporary uploads

### UI Settings  
- `show_progress_bar`: Enable/disable progress indicators
- `show_error_details`: Show detailed error information
- `auto_cleanup_temp_files`: Automatic cleanup of temporary files

### Theme Settings
- `primary_color`: Main theme color
- `background_color`: Background color
- `font`: Font family selection

### Security Settings
- `security_mode`: "strict" or "lenient" validation
- `enable_fallback_validation`: Fallback validation options
- `validation_timeout_seconds`: Validation timeout

## 🎨 Styling System

The TSS UI Kit includes a comprehensive CSS styling system:

- **Typography**: Consistent font families and sizes
- **Color Scheme**: Professional color palettes  
- **Spacing**: Optimized margins and padding
- **Responsive**: Mobile-friendly layouts
- **Components**: Styled form elements and containers

### Custom CSS Classes

Key CSS classes you can customize:

- `.upload-area-compact`: File upload styling
- `.progress-container-compact`: Progress section styling
- `.info-box`, `.success-box`, `.error-box`: Message styling
- `.step-indicator`: Progress step styling
- `.download-section`: Download area styling

## 📁 Project Structure

```
tss_ui_kit/
├── __init__.py          # Main module exports
├── components.py        # UI component classes and functions
├── styles.py           # CSS styling system
├── config.py           # Configuration management
└── README.md           # This documentation
```

## 🚦 Error Handling

The UI Kit includes robust error handling:

```python
try:
    file_data = ui.render_file_upload_area()
    # Process file...
except Exception as e:
    ui.render_error_message(f"Processing failed: {e}")
```

Built-in validation:
- File size limits
- File type checking
- Data structure validation
- Security checks

## 💡 Best Practices

1. **Use Quick Setup** for simple applications
2. **Configure themes** at application start
3. **Validate user input** before processing
4. **Show progress** for long-running operations
5. **Provide clear error messages** with helpful details
6. **Clean up temporary files** after processing
7. **Use responsive layouts** for mobile compatibility

## 🔄 Migration from TSS Converter

If migrating from the original TSS Converter:

```python
# Old way
from ui_components import render_app_header, inject_custom_css
from config_streamlit import STREAMLIT_CONFIG

# New way  
from tss_ui_kit import quick_setup
ui = quick_setup("My App")
```

The TSS UI Kit maintains full compatibility while providing better organization and reusability.

## 📄 License

Internal use - Ngoc Son Company

## 🤝 Support

For questions or issues:
1. Check this documentation
2. Review the demo application  
3. Examine the example code
4. Contact the development team

---

**Built with ❤️ by the TSS Team**