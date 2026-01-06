"""
Step 4 Duplicate Remover Module - Streamlit Interface
Wrapper around core pipeline for Step 4 duplicate removal.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
from .core_pipeline import CoreStep4DuplicateRemover

class Step4DuplicateRemover:
    """
    Streamlit wrapper for Step 4 duplicate removal processing
    Uses CoreStep4DuplicateRemover for actual processing
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the Step 4 duplicate remover
        
        Args:
            output_dir: Directory to save Step 4 files (default: ./output)
        """
        # Initialize core processor
        self.core_processor = CoreStep4DuplicateRemover(output_dir)
    
    def process_multiple_sheets_to_step4(self, step3_files: list) -> Dict[str, Any]:
        """
        Process multiple sheets from Step 3 to Step 4
        
        Args:
            step3_files: List of Step 3 files to process
            
        Returns:
            Dictionary with results and Step 4 file paths
        """
        results = {
            'success_count': 0,
            'failed_count': 0,
            'step4_files': [],
            'failed_sheets': [],
            'total_sheets': len(step3_files)
        }
        
        for step3_file in step3_files:
            try:
                sheet_name = step3_file['sheet_name']
                step3_path = step3_file['file_path']
                
                # Remove duplicates from Step 3 file
                step4_path = self.core_processor.remove_duplicates(step3_path)
                
                results['success_count'] += 1
                results['step4_files'].append({
                    'sheet_name': sheet_name,
                    'filename': Path(step4_path).name,
                    'file_path': step4_path
                })
                
            except Exception as e:
                logging.error(f"Error processing Step 4 for sheet '{sheet_name}': {str(e)}")
                results['failed_count'] += 1
                results['failed_sheets'].append(sheet_name)
        
        return results