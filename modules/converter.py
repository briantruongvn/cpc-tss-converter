"""
Template Converter Module - Streamlit Interface
Wrapper around core pipeline for Streamlit web application use.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
from .core_pipeline import CoreTemplateCreator

class TemplateConverter:
    """
    Template converter wrapper for Streamlit web application
    Uses CoreTemplateCreator for actual template creation
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the template converter
        
        Args:
            output_dir: Directory to save output files (default: ./output)
        """
        # Initialize core template creator
        self.core_creator = CoreTemplateCreator(output_dir)
    
    def create_template_for_sheet(self, sheet_name: str, original_filename: str) -> Optional[str]:
        """
        Create a Step 1 template for a specific sheet
        
        Args:
            sheet_name: Name of the sheet to create template for
            original_filename: Original filename for naming convention
            
        Returns:
            Path to created template file or None if failed
        """
        return self.core_creator.create_template(sheet_name, original_filename)
    
    def create_multiple_templates(self, sheet_names: list, original_filename: str) -> Dict[str, Any]:
        """
        Create templates for multiple sheets
        
        Args:
            sheet_names: List of sheet names to process
            original_filename: Original filename for naming convention
            
        Returns:
            Dictionary with results and file paths
        """
        results = {
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
        """
        Validate that a created template has the correct structure
        
        Args:
            template_path: Path to template file to validate
            
        Returns:
            True if valid, False otherwise
        """
        return self.core_creator.validate_template_structure(template_path)
    
    def get_output_directory(self) -> str:
        """Get the output directory path"""
        return str(self.core_creator.output_dir)
    
    def get_template_info(self) -> Dict[str, Any]:
        """
        Get information about the template structure
        
        Returns:
            Dictionary with template information
        """
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