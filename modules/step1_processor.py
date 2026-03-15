"""Step 1 processor — Streamlit wrapper around CoreTemplateCreator."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .core import CoreTemplateCreator


class TemplateConverter:
    """
    Streamlit wrapper for Step 1 template creation.
    Delegates all logic to CoreTemplateCreator.
    """

    def __init__(self, output_dir: Optional[str] = None):
        self.core_creator = CoreTemplateCreator(output_dir)

    def create_template_for_sheet(
        self, sheet_name: str, original_filename: str
    ) -> Optional[str]:
        """Create a Step 1 template for a specific sheet."""
        return self.core_creator.create_template(sheet_name, original_filename)

    def create_multiple_templates(
        self, sheet_names: list, original_filename: str
    ) -> Dict[str, Any]:
        """Create templates for multiple sheets."""
        results: Dict[str, Any] = {
            'success_count': 0,
            'failed_count': 0,
            'created_files': [],
            'failed_sheets': [],
            'total_sheets': len(sheet_names)
        }

        for sheet_name in sheet_names:
            template_path = self.create_template_for_sheet(sheet_name, original_filename)

            if template_path:
                results['success_count'] += 1
                results['created_files'].append({
                    'sheet_name': sheet_name,
                    'filename': f"{Path(original_filename).stem} - {sheet_name} - Step1.xlsx",
                    'file_path': template_path
                })
            else:
                results['failed_count'] += 1
                results['failed_sheets'].append(sheet_name)

        return results

    def validate_template_structure(self, template_path: str) -> bool:
        """Validate that a created template has the correct structure."""
        return self.core_creator.validate_template_structure(template_path)

    def get_output_directory(self) -> str:
        """Get the output directory path."""
        return str(self.core_creator.output_dir)

    def get_template_info(self) -> Dict[str, Any]:
        """Get information about the template structure."""
        headers = self.core_creator.get_template_headers()
        return {
            'header_count': len(headers),
            'columns': [h["name"] for h in headers],
            'structure': {
                'row_1': "Article name",
                'row_2': "Article number",
                'row_3': "Headers (A-Q)"
            },
            'output_format': "[base_name] - [sheet_name] - Step1.xlsx"
        }
