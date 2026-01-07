"""
TSS UI Kit - Configuration Management
Default configurations and settings for TSS UI Kit components.
"""

import os
from typing import Dict, Any, List
from pathlib import Path

# Default UI Kit Configuration
DEFAULT_CONFIG = {
    # App metadata
    "app_title": "TSS UI Kit App",
    "app_icon": "📊",
    "page_title": "TSS App",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    
    # File upload settings
    "max_file_size_mb": 50,
    "allowed_file_types": [".xlsx", ".csv", ".json"],
    "upload_directory": "temp/uploads",
    "output_directory": "temp/outputs",
    
    # UI settings
    "show_progress_bar": True,
    "show_step_details": False,
    "auto_cleanup_temp_files": True,
    "session_timeout_minutes": 30,
    
    # Processing settings
    "enable_async_processing": True,
    "max_concurrent_uploads": 3,
    "processing_timeout_minutes": 10,
    
    # Display settings
    "theme": {
        "primary_color": "#2563eb",
        "background_color": "#FFFFFF",
        "secondary_background_color": "#F0F2F6",
        "text_color": "#262730",
        "font": "sans serif"
    },
    
    # Error handling
    "show_error_details": True,
    "log_user_actions": True,
    "enable_error_reporting": True,
    
    # Security and validation settings
    "security_mode": "lenient",  # "strict" or "lenient" 
    "enable_fallback_validation": True,
    "enable_enhanced_logging": False,
    "validation_timeout_seconds": 30,
    "debug_validation": False,
    "allow_large_files": False,
    "strict_excel_validation": False
}

# Step configuration template for processing pipelines
DEFAULT_STEP_CONFIG = {
    "step1": {
        "name": "Initialize",
        "description": "Initialize processing pipeline",
        "icon": "🚀",
        "estimated_time": "1-2 seconds"
    },
    "step2": {
        "name": "Process", 
        "description": "Process uploaded data",
        "icon": "⚙️",
        "estimated_time": "5-15 seconds"
    },
    "step3": {
        "name": "Validate",
        "description": "Validate processed data",
        "icon": "✅",
        "estimated_time": "2-5 seconds"
    },
    "step4": {
        "name": "Finalize",
        "description": "Finalize and prepare output",
        "icon": "📋",
        "estimated_time": "1-3 seconds"
    }
}

# Help content template
DEFAULT_HELP_CONTENT = {
    "📋 Getting Started": """
    1. Upload your file using the file uploader
    2. Click the process button to start
    3. Wait for processing to complete
    4. Download the results
    """,
    
    "📁 File Requirements": """
    - Supported formats: Excel (.xlsx), CSV (.csv)
    - Maximum file size: 50MB
    - File should contain valid data structure
    """,
    
    "🔧 Features": """
    - Professional UI components
    - Real-time progress tracking
    - Error handling and validation
    - Customizable themes and styling
    """,
    
    "❓ Support": """
    If you encounter any issues:
    - Check file format and size requirements
    - Ensure stable internet connection
    - Contact support if problems persist
    """
}

# Theme configurations
THEME_CONFIGS = {
    "default": {
        "name": "Default",
        "description": "Clean blue theme with professional styling",
        "colors": {
            "primary": "#2563eb",
            "success": "#065f46", 
            "error": "#991b1b",
            "warning": "#92400e",
            "info": "#374151",
            "background": "#ffffff",
            "surface": "#f9fafb"
        }
    },
    
    "dark": {
        "name": "Dark",
        "description": "Dark theme for low-light environments",
        "colors": {
            "primary": "#3b82f6",
            "success": "#10b981",
            "error": "#ef4444", 
            "warning": "#f59e0b",
            "info": "#94a3b8",
            "background": "#0f172a",
            "surface": "#1e293b"
        }
    },
    
    "minimal": {
        "name": "Minimal",
        "description": "Clean minimal theme with essential styling",
        "colors": {
            "primary": "#000000",
            "success": "#16a34a",
            "error": "#dc2626",
            "warning": "#ca8a04", 
            "info": "#64748b",
            "background": "#ffffff",
            "surface": "#f8fafc"
        }
    },
    
    "corporate": {
        "name": "Corporate",
        "description": "Professional corporate theme",
        "colors": {
            "primary": "#1f2937",
            "success": "#059669",
            "error": "#dc2626",
            "warning": "#d97706",
            "info": "#6b7280",
            "background": "#ffffff",
            "surface": "#f9fafb"
        }
    }
}

class TSSUIConfig:
    """Configuration management class for TSS UI Kit"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize with optional custom config"""
        self.config = DEFAULT_CONFIG.copy()
        if config:
            self.update_config(config)
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        def deep_update(base: dict, update: dict):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_update(base[key], value)
                else:
                    base[key] = value
        
        deep_update(self.config, updates)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value by key"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_streamlit_config(self) -> Dict[str, Any]:
        """Get Streamlit page configuration"""
        return {
            "page_title": self.get("page_title", "TSS App"),
            "page_icon": self.get("app_icon", "📊"),
            "layout": self.get("layout", "wide"),
            "initial_sidebar_state": self.get("initial_sidebar_state", "expanded")
        }
    
    def get_file_upload_config(self) -> Dict[str, Any]:
        """Get file upload configuration"""
        return {
            "max_file_size_mb": self.get("max_file_size_mb", 50),
            "allowed_file_types": self.get("allowed_file_types", [".xlsx"]),
            "upload_directory": self.get("upload_directory", "temp/uploads"),
            "output_directory": self.get("output_directory", "temp/outputs")
        }
    
    def get_theme_config(self, theme_name: str = "default") -> Dict[str, Any]:
        """Get theme configuration"""
        return THEME_CONFIGS.get(theme_name, THEME_CONFIGS["default"])
    
    def get_help_content(self) -> Dict[str, str]:
        """Get help content configuration"""
        return DEFAULT_HELP_CONTENT.copy()
    
    def get_step_config(self) -> Dict[str, Dict[str, str]]:
        """Get step configuration"""
        return DEFAULT_STEP_CONFIG.copy()
    
    def apply_environment_overrides(self):
        """Apply environment-specific configuration overrides"""
        env = os.getenv("TSS_ENV", "development")
        
        if env == "production":
            self.update_config({
                "show_error_details": False,
                "log_user_actions": True,
                "max_file_size_mb": 100,
                "processing_timeout_minutes": 15,
                "security_mode": "strict"
            })
        elif env == "development":
            self.update_config({
                "show_error_details": True,
                "log_user_actions": True,
                "auto_cleanup_temp_files": False,  # Keep files for debugging
                "debug_validation": True
            })
        elif env == "testing":
            self.update_config({
                "show_error_details": True,
                "max_file_size_mb": 10,  # Smaller for tests
                "processing_timeout_minutes": 5,
                "auto_cleanup_temp_files": True
            })
    
    def export_config(self) -> Dict[str, Any]:
        """Export current configuration"""
        return self.config.copy()
    
    def load_config_file(self, file_path: str):
        """Load configuration from JSON file"""
        import json
        try:
            with open(file_path, 'r') as f:
                file_config = json.load(f)
            self.update_config(file_config)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Could not load config file {file_path}: {e}")
    
    def save_config_file(self, file_path: str):
        """Save current configuration to JSON file"""
        import json
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            raise ValueError(f"Could not save config file {file_path}: {e}")

def create_config(config_dict: Dict[str, Any] = None) -> TSSUIConfig:
    """Create a new configuration instance"""
    return TSSUIConfig(config_dict)

def get_default_config() -> Dict[str, Any]:
    """Get default configuration dictionary"""
    return DEFAULT_CONFIG.copy()

def get_step_config() -> Dict[str, Dict[str, str]]:
    """Get default step configuration"""
    return DEFAULT_STEP_CONFIG.copy()

def get_help_content() -> Dict[str, str]:
    """Get default help content"""
    return DEFAULT_HELP_CONTENT.copy()

def get_theme_config(theme_name: str = "default") -> Dict[str, Any]:
    """Get theme configuration by name"""
    return THEME_CONFIGS.get(theme_name, THEME_CONFIGS["default"])

def list_available_themes() -> List[str]:
    """List all available theme names"""
    return list(THEME_CONFIGS.keys())

def create_custom_step_config(steps: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    """
    Create custom step configuration from list of step definitions
    
    Args:
        steps: List of dicts with keys: name, description, icon, estimated_time
    
    Returns:
        Formatted step configuration dict
    """
    step_config = {}
    for i, step in enumerate(steps, 1):
        step_key = f"step{i}"
        step_config[step_key] = {
            "name": step.get("name", f"Step {i}"),
            "description": step.get("description", ""),
            "icon": step.get("icon", "⚙️"),
            "estimated_time": step.get("estimated_time", "Unknown")
        }
    return step_config

# Quick access functions for common configurations
def get_temp_directory(subdir: str = "") -> Path:
    """Get temporary directory path for file operations"""
    base_temp = Path("temp")
    if subdir:
        temp_dir = base_temp / subdir
    else:
        temp_dir = base_temp
    
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir

def get_validation_config(security_mode: str = "lenient") -> Dict[str, Any]:
    """Get validation configuration based on security mode"""
    base_config = {
        'max_file_size_mb': 50,
        'validation_timeout': 30,
        'debug_validation': False,
        'enable_enhanced_logging': False,
        'allow_large_files': False,
        'strict_excel_validation': False
    }
    
    if security_mode == "strict":
        base_config.update({
            'max_file_size_mb': 25,
            'validation_timeout': 15,
            'strict_excel_validation': True,
            'allow_large_files': False
        })
    elif security_mode == "lenient":
        base_config.update({
            'max_file_size_mb': 100,
            'validation_timeout': 60,
            'allow_large_files': True
        })
    
    return base_config