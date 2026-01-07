"""
TSS UI Kit - Reusable Streamlit Components
Professional UI components extracted from TSS Converter for reuse across projects.
"""

import streamlit as st
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
from pathlib import Path
import time
import logging
from datetime import datetime

# Set up logger
logger = logging.getLogger(__name__)

class TSSUIKit:
    """Main UI Kit class containing all reusable components"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize UI Kit with optional configuration"""
        self.config = config or self._get_default_config()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "max_file_size_mb": 50,
            "show_error_details": True,
            "compact_mode": False,
            "theme": {
                "primary_color": "#2563eb",
                "success_color": "#065f46",
                "error_color": "#991b1b",
                "warning_color": "#92400e"
            }
        }
    
    def inject_custom_css(self, hide_streamlit_branding: bool = True):
        """
        Inject custom CSS styling into Streamlit app
        
        Args:
            hide_streamlit_branding: Whether to hide Streamlit Cloud elements
        """
        from .styles import get_custom_css
        
        # Inject main CSS
        st.markdown(get_custom_css(), unsafe_allow_html=True)
        
        if hide_streamlit_branding:
            # Additional JavaScript to hide Streamlit Cloud elements
            hide_streamlit_js = """
            <script>
            function hideStreamlitCloudElements() {
                const elementsToHide = [
                    '[data-testid="stToolbar"]',
                    '[data-testid="stHeader"]', 
                    '[data-testid="stDecoration"]',
                    'header[data-testid="stHeader"]',
                    'button[title="View app source on GitHub"]',
                    'button[aria-label="Share"]',
                    'button[aria-label="Star"]', 
                    'button[aria-label="Edit"]',
                    '[data-testid="manage-app-button"]',
                    'a[href*="github.com"]',
                    '.stToolbar'
                ];
                
                elementsToHide.forEach(selector => {
                    const elements = document.querySelectorAll(selector);
                    elements.forEach(el => {
                        if (el) {
                            el.style.display = 'none !important';
                            el.style.visibility = 'hidden !important';
                            el.remove();
                        }
                    });
                });
            }
            
            hideStreamlitCloudElements();
            setTimeout(hideStreamlitCloudElements, 100);
            setTimeout(hideStreamlitCloudElements, 500);
            
            const observer = new MutationObserver(hideStreamlitCloudElements);
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true
            });
            
            setInterval(hideStreamlitCloudElements, 1000);
            </script>
            """
            st.markdown(hide_streamlit_js, unsafe_allow_html=True)

    def render_app_header(self, title: str, subtitle: Optional[str] = None, 
                         icon: str = "📊", compact: bool = False, show_line: bool = False):
        """
        Render main application header
        
        Args:
            title: Main title text
            subtitle: Optional subtitle text  
            icon: Emoji icon for title
            compact: Whether to use compact mode
            show_line: Whether to show horizontal line after subtitle
        """
        header_margin = "0.5rem auto" if compact else "0 auto"
        
        st.markdown(f"""
            <div class="app-header-container" style='text-align: center; margin: {header_margin}; max-width: 90%;'>
                <h1 class="compact-title">{icon} {title}</h1>
                {f'<p class="compact-subtitle">{subtitle}</p>' if subtitle else ''}
            </div>
        """, unsafe_allow_html=True)
        
        if not compact:
            st.markdown("""
                <div style='text-align: center; margin: 1.5rem auto;'>
                    <hr style='width: 60%; max-width: 600px; margin: 0 auto; border: none; border-top: 1px solid #e5e7eb;'>
                </div>
            """, unsafe_allow_html=True)
        elif show_line:
            # Show line for compact mode when requested
            st.markdown("""
                <div style='text-align: center; margin: 1rem auto;'>
                    <hr style='width: 60%; max-width: 600px; margin: 0 auto; border: none; border-top: 1px solid #e5e7eb;'>
                </div>
            """, unsafe_allow_html=True)

    def render_file_upload_area(self, accepted_types: List[str] = None, 
                               help_text: str = None) -> Optional[Tuple[bytes, str]]:
        """
        Render file upload area with validation
        
        Args:
            accepted_types: List of accepted file extensions (e.g., ['xlsx', 'csv'])
            help_text: Custom help text for file uploader
            
        Returns:
            Tuple of (file_bytes, filename) if valid file uploaded, None otherwise
        """
        if accepted_types is None:
            accepted_types = ["xlsx"]
        
        max_size = self.config.get("max_file_size_mb", 50)
        help_text = help_text or f"Maximum file size: {max_size}MB"
        
        st.markdown("""
            <div class="upload-area-compact">
                <h4 class="upload-title">📁 Upload File</h4>
                <p class="upload-subtitle">Select file to process</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            label="Select file",
            type=accepted_types,
            help=help_text,
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Validate file size
            file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
            if file_size_mb > max_size:
                self.render_error_message(f"File too large! Maximum size: {max_size}MB")
                return None
            
            # Display file info
            self.render_info_message(f"✅ File uploaded: {uploaded_file.name} ({file_size_mb:.1f}MB)")
            return uploaded_file.getvalue(), uploaded_file.name
        
        return None

    def render_progress_section(self, current_step: int = 0, 
                               step_status: Dict[str, str] = None,
                               step_config: Dict[str, Dict[str, str]] = None,
                               compact: bool = True):
        """
        Render progress section with step indicators
        
        Args:
            current_step: Current step number
            step_status: Dict with step status ('pending', 'running', 'completed', 'error')
            step_config: Configuration for each step (name, description, etc.)
            compact: Whether to use compact mode
        """
        if step_status is None:
            step_status = {}
        if step_config is None:
            step_config = {}
        
        container_class = "progress-container-compact" if compact else "progress-container"
        
        st.markdown(f"""
            <div class="{container_class}">
                <h4 class="progress-title">🔄 Processing</h4>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate progress percentage
        total_steps = len(step_status) if step_status else 5
        completed_steps = sum(1 for status in step_status.values() if status == "completed")
        running_steps = sum(1 for status in step_status.values() if status == "running")
        
        progress_value = (completed_steps + (0.5 if running_steps > 0 else 0)) / total_steps
        progress_percentage = int(progress_value * 100)
        
        # Progress bar
        progress_text = f"📊 {progress_percentage}% ({completed_steps}/{total_steps} steps)"
        st.progress(progress_value, text=progress_text)
        
        # Step status display
        if compact:
            if running_steps > 0:
                current_step_info = step_config.get(f"step{current_step}", {})
                current_step_name = current_step_info.get('name', f'Step {current_step}')
                st.info(f"⏳ {current_step_name}...")
            elif completed_steps == total_steps:
                st.success("✅ Completed!")
            elif any(status == "error" for status in step_status.values()):
                st.error("❌ Error occurred")
        else:
            # Full status display with step details
            for step_key, status in step_status.items():
                step_info = step_config.get(step_key, {})
                
                if status == "completed":
                    icon = "✅"
                    css_class = "step-completed"
                elif status == "running":
                    icon = "⏳"
                    css_class = "step-running"
                elif status == "error":
                    icon = "❌"
                    css_class = "step-error"
                else:
                    icon = "⏸️"
                    css_class = "step-pending"
                
                time_info = ""
                if status == "running" and step_info.get('estimated_time'):
                    time_info = f"<br><small>⏱️ Estimated: {step_info['estimated_time']}</small>"
                
                st.markdown(f"""
                    <div class="step-indicator {css_class}">
                        <strong>{icon} {step_info.get('name', step_key)}</strong><br>
                        <small>{step_info.get('description', '')}</small>
                        {time_info}
                    </div>
                """, unsafe_allow_html=True)

    def generate_download_filename(self, original_name: Optional[str] = None, 
                                  suffix: str = "Processed") -> str:
        """
        Generate download filename with timestamp
        
        Args:
            original_name: Original filename
            suffix: Suffix to add (default: "Processed")
            
        Returns:
            Formatted filename
        """
        timestamp = datetime.now().strftime("%Y%m%d")
        
        if original_name:
            clean_name = original_name
            # Remove file extension
            if '.' in clean_name:
                name_part = clean_name.rsplit('.', 1)[0]
                ext = clean_name.rsplit('.', 1)[1]
                return f"{name_part}_{suffix}_{timestamp}.{ext}"
            else:
                return f"{clean_name}_{suffix}_{timestamp}"
        else:
            return f"Output_{suffix}_{timestamp}"

    def render_download_section(self, file_path: Optional[Union[str, Path]] = None,
                               original_filename: Optional[str] = None,
                               custom_filename: Optional[str] = None):
        """
        Render download section for output files
        
        Args:
            file_path: Path to output file
            original_filename: Original uploaded filename for naming
            custom_filename: Custom download filename
        """
        # Convert to Path object if needed
        if file_path and isinstance(file_path, str):
            file_path = Path(file_path)
        
        if file_path and file_path.exists():
            st.markdown("""
                <div class="download-section">
                    <h3>🎉 Processing Complete!</h3>
                    <p>File has been processed successfully. Click to download.</p>
                </div>
            """, unsafe_allow_html=True)
            
            try:
                with open(file_path, "rb") as file:
                    file_data = file.read()
                
                # Generate download filename
                download_filename = custom_filename or self.generate_download_filename(original_filename)
                
                # Determine MIME type based on file extension
                mime_type = "application/octet-stream"
                if str(file_path).lower().endswith('.xlsx'):
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif str(file_path).lower().endswith('.csv'):
                    mime_type = "text/csv"
                
                # Create centered HTML download button
                import base64
                b64 = base64.b64encode(file_data).decode()
                
                st.markdown(f"""
                    <div style="display: flex; justify-content: center; align-items: center; margin: 1rem 0;">
                        <a href="data:{mime_type};base64,{b64}" 
                           download="{download_filename}"
                           style="
                               display: inline-flex;
                               align-items: center;
                               justify-content: center;
                               padding: 0.5rem 1rem;
                               background-color: #2563eb !important;
                               color: #ffffff !important;
                               text-decoration: none;
                               border-radius: 6px;
                               font-size: 0.875rem;
                               font-weight: 500;
                               font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
                               transition: all 0.15s ease;
                               border: 1px solid #2563eb !important;
                               cursor: pointer;
                               gap: 0.5rem;
                               box-shadow: none;
                           "
                           onmouseover="this.style.backgroundColor='#1d4ed8'; this.style.borderColor='#1d4ed8'"
                           onmouseout="this.style.backgroundColor='#2563eb'; this.style.borderColor='#2563eb'"
                           title="Click to download the processed file">
                            📥 Download Processed File
                        </a>
                    </div>
                """, unsafe_allow_html=True)
                
                    
            except Exception as e:
                self.render_error_message(f"Error preparing download: {str(e)}")
        else:
            self.render_warning_message("Output file is not ready for download yet.")


    def render_info_message(self, message: str):
        """Render info message box"""
        st.markdown(f"""
            <div class="info-box">
                ℹ️ {message}
            </div>
        """, unsafe_allow_html=True)

    def render_success_message(self, message: str):
        """Render success message box"""
        st.markdown(f"""
            <div class="info-box success-box">
                ✅ {message}
            </div>
        """, unsafe_allow_html=True)

    def render_warning_message(self, message: str):
        """Render warning message box"""
        st.markdown(f"""
            <div class="info-box warning-box">
                ⚠️ {message}
            </div>
        """, unsafe_allow_html=True)

    def render_error_message(self, message: str, details: Optional[str] = None):
        """Render error message box with optional details"""
        st.markdown(f"""
            <div class="info-box error-box">
                ❌ {message}
            </div>
        """, unsafe_allow_html=True)
        
        if details and self.config.get("show_error_details", True):
            with st.expander("Error Details"):
                st.code(details)

    def render_help_section(self, help_content: Dict[str, str], sidebar: bool = True):
        """
        Render help section
        
        Args:
            help_content: Dict with help sections and content
            sidebar: Whether to render in sidebar
        """
        container = st.sidebar if sidebar else st
        
        with container:
            container.markdown("## 📖 Help")
            
            for section, content in help_content.items():
                container.markdown(f"### {section}")
                container.markdown(content)

    def render_footer(self, app_name: str = "TSS UI Kit App", version: str = "1.0"):
        """Render application footer"""
        st.markdown(f"""
            <div class="footer">
                <p>
                    🛠️ {app_name} v{version} | 
                    Powered by Streamlit | 
                    Built with TSS UI Kit
                </p>
            </div>
        """, unsafe_allow_html=True)

    def create_columns(self, ratios: List[float]) -> Tuple[Any, ...]:
        """Create column layout with specified ratios"""
        return st.columns(ratios)

    def display_loading_spinner(self, message: str = "Processing..."):
        """Display loading spinner with message"""
        return st.spinner(message)

    def render_action_button(self, label: str, key: Optional[str] = None, 
                            button_type: str = "primary", 
                            disabled: bool = False, 
                            help_text: Optional[str] = None,
                            on_click: Optional[Callable] = None) -> bool:
        """
        Render action button with consistent styling
        
        Args:
            label: Button text
            key: Unique key for button
            button_type: 'primary' or 'secondary'
            disabled: Whether button is disabled
            help_text: Help tooltip text
            on_click: Callback function
            
        Returns:
            True if button was clicked
        """
        return st.button(
            label=label,
            key=key,
            type=button_type,
            disabled=disabled,
            help=help_text,
            on_click=on_click
        )

    def clear_temp_files_button(self, temp_dir: Union[str, Path] = "temp"):
        """Render button to clear temporary files"""
        if st.button("🗑️ Clear Temp Files", help="Delete all temporary files"):
            try:
                temp_path = Path(temp_dir)
                if temp_path.exists():
                    import shutil
                    shutil.rmtree(temp_path)
                    self.render_success_message("Temporary files cleared successfully")
                    st.rerun()
            except Exception as e:
                self.render_error_message(f"Unable to clear temp files: {str(e)}")

# Convenience functions for direct use
def create_ui_kit(config: Optional[Dict[str, Any]] = None) -> TSSUIKit:
    """Create a new UI Kit instance"""
    return TSSUIKit(config)

def inject_css(hide_branding: bool = True):
    """Quick function to inject CSS"""
    kit = TSSUIKit()
    kit.inject_custom_css(hide_branding)