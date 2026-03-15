"""Configuration manager for the TSS pipeline."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Manages configuration loading and caching"""

    _template_config = None
    _processing_config = None

    @classmethod
    def get_template_config(cls, config_dir: Optional[str] = None) -> Dict[str, Any]:
        """Load template configuration from JSON file"""
        if cls._template_config is None:
            if config_dir:
                config_path = Path(config_dir) / "template_config.json"
            else:
                # modules/core/ → modules/ → project_root/ → config/
                config_path = Path(__file__).parent.parent.parent / "config" / "template_config.json"

            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    cls._template_config = json.load(f)
            except Exception as e:
                logging.error(f"Failed to load template config: {e}")
                raise

        return cls._template_config

    @classmethod
    def get_processing_config(cls, config_dir: Optional[str] = None) -> Dict[str, Any]:
        """Load processing configuration from JSON file"""
        if cls._processing_config is None:
            if config_dir:
                config_path = Path(config_dir) / "processing_config.json"
            else:
                config_path = Path(__file__).parent.parent.parent / "config" / "processing_config.json"

            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    cls._processing_config = json.load(f)
            except Exception as e:
                logging.error(f"Failed to load processing config: {e}")
                raise

        return cls._processing_config

    @classmethod
    def reload_configs(cls):
        """Force reload of configurations"""
        cls._template_config = None
        cls._processing_config = None
