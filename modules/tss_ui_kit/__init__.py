"""
TSS UI Kit - Professional Streamlit Components Library

A comprehensive UI component library extracted from the TSS Converter project.
Provides reusable, professional-grade Streamlit components for building
data processing web applications.

Features:
- Professional UI components (headers, upload areas, progress tracking)
- Complete CSS styling system with multiple themes
- Configurable settings and validation
- File processing utilities
- Error handling and messaging
- Progress tracking and statistics display

Quick Start:
    ```python
    import streamlit as st
    from tss_ui_kit import TSSUIKit, create_config
    
    # Initialize UI Kit
    config = create_config({
        "app_title": "My App",
        "max_file_size_mb": 100
    })
    ui = TSSUIKit(config)
    
    # Set up page
    st.set_page_config(**config.get_streamlit_config())
    ui.inject_custom_css()
    
    # Render components
    ui.render_app_header("My Application", "Process your data")
    file_data = ui.render_file_upload_area()
    
    if file_data:
        ui.render_success_message("File uploaded successfully!")
    ```

Author: TSS Team
Version: 1.0
License: Internal Use
"""

__version__ = "1.0.0"
__author__ = "TSS Team"

# Core components
from .components import (
    TSSUIKit,
    create_ui_kit,
    inject_css
)

# Configuration management
from .config import (
    TSSUIConfig,
    create_config,
    get_default_config,
    get_step_config,
    get_help_content,
    get_theme_config,
    list_available_themes,
    create_custom_step_config,
    get_temp_directory,
    get_validation_config,
    DEFAULT_CONFIG,
    DEFAULT_STEP_CONFIG,
    DEFAULT_HELP_CONTENT,
    THEME_CONFIGS
)

# Styling system
from .styles import (
    get_custom_css,
    get_dark_theme_css,
    get_minimal_css,
    THEMES
)

# Convenience imports for common use cases
__all__ = [
    # Main classes
    "TSSUIKit",
    "TSSUIConfig",
    
    # Factory functions
    "create_ui_kit",
    "create_config",
    "inject_css",
    
    # Configuration functions
    "get_default_config",
    "get_step_config", 
    "get_help_content",
    "get_theme_config",
    "list_available_themes",
    "create_custom_step_config",
    "get_temp_directory",
    "get_validation_config",
    
    # Styling functions
    "get_custom_css",
    "get_dark_theme_css", 
    "get_minimal_css",
    
    # Constants
    "DEFAULT_CONFIG",
    "DEFAULT_STEP_CONFIG", 
    "DEFAULT_HELP_CONTENT",
    "THEME_CONFIGS",
    "THEMES"
]

# Quick setup function for common use case
def quick_setup(app_title: str = "TSS App", 
                theme: str = "default",
                max_file_size_mb: int = 50,
                hide_branding: bool = True) -> TSSUIKit:
    """
    Quick setup function for common TSS UI Kit usage
    
    Args:
        app_title: Application title
        theme: Theme name ("default", "dark", "minimal", "corporate")
        max_file_size_mb: Maximum file upload size
        hide_branding: Whether to hide Streamlit branding
    
    Returns:
        Configured TSSUIKit instance
        
    Example:
        ```python
        import streamlit as st
        from tss_ui_kit import quick_setup
        
        # Quick setup
        ui = quick_setup("My Data Processor", theme="dark")
        
        # Use components
        ui.render_app_header("My App", "Process your files")
        file_data = ui.render_file_upload_area()
        ```
    """
    import streamlit as st
    
    # Create config with custom settings
    config = create_config({
        "app_title": app_title,
        "page_title": app_title,
        "max_file_size_mb": max_file_size_mb
    })
    
    # Set up Streamlit page
    st.set_page_config(**config.get_streamlit_config())
    
    # Create UI Kit instance
    ui = TSSUIKit(config.export_config())
    
    # Apply styling
    if theme == "dark":
        ui.inject_custom_css(hide_branding)
        st.markdown(get_dark_theme_css(), unsafe_allow_html=True)
    elif theme == "minimal":
        st.markdown(get_minimal_css(), unsafe_allow_html=True)
    else:
        ui.inject_custom_css(hide_branding)
    
    return ui

# Version info
def get_version_info():
    """Get version information"""
    return {
        "version": __version__,
        "author": __author__,
        "components": len([
            "TSSUIKit", "TSSUIConfig", "render_app_header", 
            "render_file_upload_area", "render_progress_section",
            "render_download_section", "render_processing_stats"
        ]),
        "themes": len(THEME_CONFIGS),
        "features": [
            "Professional UI Components",
            "Multiple Themes Support", 
            "Configuration Management",
            "File Upload Validation",
            "Progress Tracking",
            "Error Handling",
            "Statistics Display",
            "Responsive Design",
            "Streamlit Branding Removal"
        ]
    }

# Example usage in docstring
"""
Complete Example:
    ```python
    import streamlit as st
    from tss_ui_kit import TSSUIKit, create_config, get_step_config
    
    # Configure app
    config = create_config({
        "app_title": "Data Processor",
        "max_file_size_mb": 100,
        "theme": {"primary_color": "#1f2937"}
    })
    
    st.set_page_config(**config.get_streamlit_config())
    
    # Create UI Kit
    ui = TSSUIKit(config.export_config())
    ui.inject_custom_css()
    
    # Build UI
    ui.render_app_header(
        title="Advanced Data Processor",
        subtitle="Upload and process your Excel files",
        icon="⚡"
    )
    
    # File upload
    file_data = ui.render_file_upload_area(
        accepted_types=["xlsx", "csv"],
        help_text="Upload Excel or CSV files up to 100MB"
    )
    
    if file_data:
        file_bytes, filename = file_data
        ui.render_info_message(f"Processing {filename}...")
        
        # Simulate processing with progress
        step_config = get_step_config()
        step_status = {"step1": "completed", "step2": "running", "step3": "pending"}
        
        ui.render_progress_section(
            current_step=2,
            step_status=step_status,
            step_config=step_config
        )
        
        # Show results
        ui.render_success_message("Processing completed!")
        
        # Download section
        ui.render_download_section(
            file_path="output.xlsx",
            original_filename=filename,
            processing_stats={
                "initial_rows": 1000,
                "final_rows": 950, 
                "processing_time": 15.5
            }
        )
    
    # Help in sidebar
    help_content = config.get_help_content()
    ui.render_help_section(help_content)
    
    # Footer
    ui.render_footer("Data Processor", "2.0")
    ```
"""