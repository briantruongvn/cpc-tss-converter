"""
File Exporter Module
Handles file export and download functionality for the TSS Converter web application.
"""

import io
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional
import tempfile
import os
import logging

class FileExporter:
    """Handles file export and download operations"""
    
    def __init__(self):
        """Initialize the file exporter"""
        self.temp_files = []
    
    def create_zip_download(self, file_list: List[Dict[str, Any]]) -> bytes:
        """
        Create a ZIP file containing multiple template files for download
        
        Args:
            file_list: List of dictionaries containing file information
                      Each dict should have: 'filename', 'file_path', 'sheet_name'
                      
        Returns:
            Bytes object containing the ZIP file data
        """
        try:
            # Create a BytesIO buffer to hold the ZIP file
            zip_buffer = io.BytesIO()
            
            # Create ZIP file
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_info in file_list:
                    file_path = file_info['file_path']
                    filename = file_info['filename']
                    
                    # Add file to ZIP
                    if os.path.exists(file_path):
                        zip_file.write(file_path, filename)
                    else:
                        logging.warning(f"File not found for ZIP: {file_path}")
            
            # Get the ZIP file bytes
            zip_buffer.seek(0)
            zip_bytes = zip_buffer.getvalue()
            zip_buffer.close()
            
            return zip_bytes
            
        except Exception as e:
            logging.error(f"Error creating ZIP file: {str(e)}")
            raise Exception(f"Failed to create ZIP download: {str(e)}")
    
    def prepare_single_file_download(self, file_path: str) -> bytes:
        """
        Prepare a single file for download
        
        Args:
            file_path: Path to the file to prepare for download
            
        Returns:
            Bytes object containing the file data
        """
        try:
            with open(file_path, 'rb') as file:
                file_bytes = file.read()
            return file_bytes
            
        except Exception as e:
            logging.error(f"Error preparing file download: {str(e)}")
            raise Exception(f"Failed to prepare file for download: {str(e)}")
    
    def get_download_filename(self, original_filename: str, sheet_name: str) -> str:
        """
        Generate download filename based on naming convention
        
        Args:
            original_filename: Original uploaded file name
            sheet_name: Name of the sheet
            
        Returns:
            Formatted filename for download
        """
        # Remove extension from original filename
        base_name = Path(original_filename).stem
        
        # Create filename following the pattern: [Input filename] - [SheetName] - Step1.xlsx
        download_filename = f"{base_name} - {sheet_name} - Step1.xlsx"
        
        return download_filename
    
    def get_zip_filename(self, original_filename: str) -> str:
        """
        Generate ZIP filename for bulk download
        
        Args:
            original_filename: Original uploaded file name
            
        Returns:
            Formatted ZIP filename
        """
        base_name = Path(original_filename).stem
        return f"{base_name}_Step1_Templates.zip"
    
    def validate_file_exists(self, file_path: str) -> bool:
        """
        Validate that a file exists and is readable
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if file exists and is readable, False otherwise
        """
        try:
            return os.path.exists(file_path) and os.path.isfile(file_path) and os.access(file_path, os.R_OK)
        except Exception:
            return False
    
    def get_file_size(self, file_path: str) -> Optional[int]:
        """
        Get the size of a file in bytes
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes, or None if file doesn't exist
        """
        try:
            if self.validate_file_exists(file_path):
                return os.path.getsize(file_path)
            return None
        except Exception:
            return None
    
    def format_file_size(self, size_bytes: int) -> str:
        """
        Format file size in a human-readable format
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string (e.g., "1.5 MB", "256 KB")
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{round(size_bytes / 1024, 1)} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{round(size_bytes / (1024 * 1024), 1)} MB"
        else:
            return f"{round(size_bytes / (1024 * 1024 * 1024), 1)} GB"
    
    def create_download_summary(self, file_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a summary of files prepared for download
        
        Args:
            file_list: List of file information dictionaries
            
        Returns:
            Summary dictionary with download statistics
        """
        try:
            summary = {
                'total_files': len(file_list),
                'valid_files': 0,
                'invalid_files': 0,
                'total_size_bytes': 0,
                'files_detail': []
            }
            
            for file_info in file_list:
                file_path = file_info['file_path']
                filename = file_info['filename']
                
                if self.validate_file_exists(file_path):
                    file_size = self.get_file_size(file_path)
                    summary['valid_files'] += 1
                    if file_size:
                        summary['total_size_bytes'] += file_size
                    
                    summary['files_detail'].append({
                        'filename': filename,
                        'sheet_name': file_info.get('sheet_name', 'Unknown'),
                        'size_bytes': file_size,
                        'size_formatted': self.format_file_size(file_size) if file_size else 'Unknown',
                        'status': 'valid'
                    })
                else:
                    summary['invalid_files'] += 1
                    summary['files_detail'].append({
                        'filename': filename,
                        'sheet_name': file_info.get('sheet_name', 'Unknown'),
                        'size_bytes': 0,
                        'size_formatted': 'File not found',
                        'status': 'invalid'
                    })
            
            summary['total_size_formatted'] = self.format_file_size(summary['total_size_bytes'])
            
            return summary
            
        except Exception as e:
            logging.error(f"Error creating download summary: {str(e)}")
            return {
                'total_files': 0,
                'valid_files': 0,
                'invalid_files': 0,
                'total_size_bytes': 0,
                'total_size_formatted': '0 B',
                'files_detail': []
            }
    
    def cleanup_temp_files(self):
        """Clean up any temporary files created during processing"""
        try:
            for temp_file in self.temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            self.temp_files.clear()
        except Exception as e:
            logging.warning(f"Error cleaning up temporary files: {str(e)}")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.cleanup_temp_files()