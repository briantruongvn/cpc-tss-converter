"""
Step 2 Processor Module - Streamlit Interface
Wrapper around core pipeline for Step 2 processing.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
from streamlit.runtime.uploaded_file_manager import UploadedFile
from .core_pipeline import CoreStep2Processor

class Step2Processor:
    """
    Streamlit wrapper for Step 2 processing
    Uses CoreStep2Processor for actual processing
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the Step 2 processor
        
        Args:
            output_dir: Directory to save Step 2 files (default: ./output)
        """
        # Initialize core processor
        self.core_processor = CoreStep2Processor(output_dir)
    
    def process_multiple_sheets_to_step2(self, uploaded_file: UploadedFile, step1_files: list) -> Dict[str, Any]:
        """
        Process multiple sheets from Step 1 to Step 2
        
        Args:
            uploaded_file: Original uploaded file for data extraction
            step1_files: List of Step 1 files to process
            
        Returns:
            Dictionary with results and Step 2 file paths
        """
        results = {
            'success_count': 0,
            'failed_count': 0,
            'step2_files': [],
            'failed_sheets': [],
            'total_sheets': len(step1_files)
        }
        
        for step1_file in step1_files:
            try:
                sheet_name = step1_file['sheet_name']
                template_path = step1_file['file_path']
                
                # Extract article information
                article_name, article_number = self.core_processor.extract_article_info_from_uploaded_file(
                    uploaded_file, sheet_name
                )
                
                # Populate template with extracted information
                step2_path = self.core_processor.populate_template_with_article_info(
                    template_path, article_name, article_number
                )
                
                results['success_count'] += 1
                results['step2_files'].append({
                    'sheet_name': sheet_name,
                    'filename': Path(step2_path).name,
                    'file_path': step2_path
                })
                
            except Exception as e:
                logging.error(f"Error processing Step 2 for sheet '{sheet_name}': {str(e)}")
                results['failed_count'] += 1
                results['failed_sheets'].append(sheet_name)
        
        return results