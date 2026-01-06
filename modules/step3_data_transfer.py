"""
Step 3 Data Transfer Module - Streamlit Interface
Wrapper around core pipeline for Step 3 data transfer.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
from streamlit.runtime.uploaded_file_manager import UploadedFile
from .core_pipeline import CoreStep3DataTransfer

class Step3DataTransfer:
    """
    Streamlit wrapper for Step 3 data transfer processing
    Uses CoreStep3DataTransfer for actual processing
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the Step 3 data transfer processor
        
        Args:
            output_dir: Directory to save Step 3 files (default: ./output)
        """
        # Initialize core processor
        self.core_processor = CoreStep3DataTransfer(output_dir)
    
    def process_multiple_sheets_to_step3(self, uploaded_file: UploadedFile, step2_files: list) -> Dict[str, Any]:
        """
        Process multiple sheets from Step 2 to Step 3
        
        Args:
            uploaded_file: Original uploaded file for data extraction
            step2_files: List of Step 2 files to process
            
        Returns:
            Dictionary with results and Step 3 file paths
        """
        results = {
            'success_count': 0,
            'failed_count': 0,
            'step3_files': [],
            'failed_sheets': [],
            'total_sheets': len(step2_files)
        }
        
        for step2_file in step2_files:
            try:
                sheet_name = step2_file['sheet_name']
                step2_path = step2_file['file_path']
                
                # Transfer data from original file to Step 2 template
                step3_path = self.core_processor.transfer_data(
                    step2_path, uploaded_file, sheet_name
                )
                
                results['success_count'] += 1
                results['step3_files'].append({
                    'sheet_name': sheet_name,
                    'filename': Path(step3_path).name,
                    'file_path': step3_path
                })
                
            except Exception as e:
                logging.error(f"Error processing Step 3 for sheet '{sheet_name}': {str(e)}")
                results['failed_count'] += 1
                results['failed_sheets'].append(sheet_name)
        
        return results