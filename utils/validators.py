"""
Validators Module
Contains validation functions for the TSS Converter web application.
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import tempfile
import os
from streamlit.runtime.uploaded_file_manager import UploadedFile
import logging

class FileValidator:
    """Handles validation of uploaded files and data"""
    
    def __init__(self):
        """Initialize the file validator"""
        self.max_file_size_mb = 200
        self.max_file_size_bytes = self.max_file_size_mb * 1024 * 1024
        self.supported_extensions = ['.xlsx', '.xls']
        self.min_sheets = 1
        self.max_sheets = 50
    
    def validate_excel_file(self, uploaded_file: UploadedFile) -> Tuple[bool, str]:
        """
        Comprehensive validation of uploaded Excel file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check if file exists
            if uploaded_file is None:
                return False, "No file uploaded"
            
            # Validate file size
            is_valid, message = self.validate_file_size(uploaded_file)
            if not is_valid:
                return False, message
            
            # Validate file extension
            is_valid, message = self.validate_file_extension(uploaded_file)
            if not is_valid:
                return False, message
            
            # Validate file format and readability
            is_valid, message = self.validate_file_format(uploaded_file)
            if not is_valid:
                return False, message
            
            # Validate file content
            is_valid, message = self.validate_file_content(uploaded_file)
            if not is_valid:
                return False, message
            
            return True, "File validation successful"
            
        except Exception as e:
            logging.error(f"Error during file validation: {str(e)}")
            return False, f"Validation error: {str(e)}"
    
    def validate_file_size(self, uploaded_file: UploadedFile) -> Tuple[bool, str]:
        """
        Validate file size is within acceptable limits
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            file_size = uploaded_file.size
            
            if file_size == 0:
                return False, "File is empty"
            
            if file_size > self.max_file_size_bytes:
                size_mb = round(file_size / (1024 * 1024), 1)
                return False, f"File too large ({size_mb}MB). Maximum allowed: {self.max_file_size_mb}MB"
            
            return True, f"File size OK ({round(file_size / (1024 * 1024), 1)}MB)"
            
        except Exception as e:
            return False, f"Error checking file size: {str(e)}"
    
    def validate_file_extension(self, uploaded_file: UploadedFile) -> Tuple[bool, str]:
        """
        Validate file has supported extension
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            file_ext = Path(uploaded_file.name).suffix.lower()
            
            if file_ext not in self.supported_extensions:
                return False, f"Unsupported file type '{file_ext}'. Supported: {', '.join(self.supported_extensions)}"
            
            return True, f"File extension OK ({file_ext})"
            
        except Exception as e:
            return False, f"Error checking file extension: {str(e)}"
    
    def validate_file_format(self, uploaded_file: UploadedFile) -> Tuple[bool, str]:
        """
        Validate file is a valid Excel format that can be read
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Create temporary file to test reading
            file_ext = Path(uploaded_file.name).suffix.lower()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.flush()
                
                try:
                    # Try to read the file
                    engine = 'openpyxl' if file_ext == '.xlsx' else 'xlrd'
                    sheets_dict = pd.read_excel(
                        tmp_file.name,
                        sheet_name=None,
                        engine=engine
                    )
                    
                    # Clean up temp file
                    os.unlink(tmp_file.name)
                    
                    # Check if we got any sheets
                    if not sheets_dict:
                        return False, "No sheets found in Excel file"
                    
                    return True, f"Excel format valid ({len(sheets_dict)} sheets found)"
                    
                except Exception as read_error:
                    # Clean up temp file
                    if os.path.exists(tmp_file.name):
                        os.unlink(tmp_file.name)
                    return False, f"Cannot read Excel file: {str(read_error)}"
                    
        except Exception as e:
            return False, f"Error validating Excel format: {str(e)}"
    
    def validate_file_content(self, uploaded_file: UploadedFile) -> Tuple[bool, str]:
        """
        Validate the content of the Excel file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            file_ext = Path(uploaded_file.name).suffix.lower()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.flush()
                
                try:
                    engine = 'openpyxl' if file_ext == '.xlsx' else 'xlrd'
                    sheets_dict = pd.read_excel(
                        tmp_file.name,
                        sheet_name=None,
                        engine=engine
                    )
                    
                    # Clean up temp file
                    os.unlink(tmp_file.name)
                    
                    # Validate number of sheets
                    sheet_count = len(sheets_dict)
                    if sheet_count < self.min_sheets:
                        return False, f"Too few sheets ({sheet_count}). Minimum: {self.min_sheets}"
                    
                    if sheet_count > self.max_sheets:
                        return False, f"Too many sheets ({sheet_count}). Maximum: {self.max_sheets}"
                    
                    # Check for non-empty sheets
                    non_empty_sheets = []
                    for sheet_name, df in sheets_dict.items():
                        if not df.empty and not df.isnull().all().all():
                            non_empty_sheets.append(sheet_name)
                    
                    if not non_empty_sheets:
                        return False, "No non-empty sheets found in the Excel file"
                    
                    return True, f"Content validation passed ({len(non_empty_sheets)} non-empty sheets)"
                    
                except Exception as content_error:
                    # Clean up temp file
                    if os.path.exists(tmp_file.name):
                        os.unlink(tmp_file.name)
                    return False, f"Error validating content: {str(content_error)}"
                    
        except Exception as e:
            return False, f"Error during content validation: {str(e)}"
    
    def validate_sheet_name(self, sheet_name: str) -> Tuple[bool, str]:
        """
        Validate sheet name for output filename compatibility
        
        Args:
            sheet_name: Name of the sheet to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            if not sheet_name or sheet_name.strip() == "":
                return False, "Sheet name is empty"
            
            # Check for invalid filename characters
            invalid_chars = ['/', '\\', '?', '*', ':', '|', '"', '<', '>']
            for char in invalid_chars:
                if char in sheet_name:
                    return False, f"Sheet name contains invalid character: '{char}'"
            
            # Check length
            if len(sheet_name) > 100:
                return False, f"Sheet name too long ({len(sheet_name)} chars). Maximum: 100"
            
            return True, "Sheet name is valid"
            
        except Exception as e:
            return False, f"Error validating sheet name: {str(e)}"
    
    def get_validation_summary(self, uploaded_file: UploadedFile) -> Dict[str, Any]:
        """
        Get comprehensive validation summary
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary with validation details
        """
        try:
            summary = {
                'filename': uploaded_file.name if uploaded_file else "No file",
                'validations': {},
                'overall_valid': False,
                'error_messages': [],
                'warnings': []
            }
            
            if uploaded_file is None:
                summary['error_messages'].append("No file uploaded")
                return summary
            
            # Run all validations
            validations = [
                ('file_size', self.validate_file_size),
                ('file_extension', self.validate_file_extension),
                ('file_format', self.validate_file_format),
                ('file_content', self.validate_file_content)
            ]
            
            all_valid = True
            for validation_name, validation_func in validations:
                try:
                    is_valid, message = validation_func(uploaded_file)
                    summary['validations'][validation_name] = {
                        'valid': is_valid,
                        'message': message
                    }
                    
                    if not is_valid:
                        all_valid = False
                        summary['error_messages'].append(f"{validation_name}: {message}")
                        
                except Exception as e:
                    all_valid = False
                    error_msg = f"{validation_name}: Validation failed - {str(e)}"
                    summary['validations'][validation_name] = {
                        'valid': False,
                        'message': error_msg
                    }
                    summary['error_messages'].append(error_msg)
            
            summary['overall_valid'] = all_valid
            
            return summary
            
        except Exception as e:
            return {
                'filename': "Unknown",
                'validations': {},
                'overall_valid': False,
                'error_messages': [f"Validation summary failed: {str(e)}"],
                'warnings': []
            }