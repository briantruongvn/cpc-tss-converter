"""
Excel File Handler Module
Handles reading and processing Excel files for the TSS Converter web application.
"""

import pandas as pd
import openpyxl
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import tempfile
import io
from streamlit.runtime.uploaded_file_manager import UploadedFile

class ExcelFileHandler:
    """Handles Excel file operations for the web application"""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls']
    
    def get_file_info(self, uploaded_file: UploadedFile) -> Dict[str, Any]:
        """
        Extract basic information about the uploaded Excel file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary containing file information
        """
        try:
            # Get file size in a readable format
            file_size_bytes = uploaded_file.size
            file_size_mb = round(file_size_bytes / (1024 * 1024), 2)
            
            if file_size_mb < 1:
                size_str = f"{round(file_size_bytes / 1024, 1)} KB"
            else:
                size_str = f"{file_size_mb} MB"
            
            # Read the file to count sheets
            sheets_data = self.read_excel_sheets(uploaded_file)
            non_empty_sheets = [name for name, df in sheets_data.items() if not df.empty]
            
            return {
                'filename': uploaded_file.name,
                'size': size_str,
                'size_bytes': file_size_bytes,
                'sheet_count': len(sheets_data),
                'non_empty_sheets': len(non_empty_sheets),
                'sheet_names': list(sheets_data.keys()),
                'non_empty_sheet_names': non_empty_sheets
            }
            
        except Exception as e:
            raise Exception(f"Error reading file information: {str(e)}")
    
    def read_excel_sheets(self, uploaded_file: UploadedFile) -> Dict[str, pd.DataFrame]:
        """
        Read all sheets from an Excel file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary mapping sheet names to DataFrames
        """
        try:
            # Create a temporary file to work with
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.flush()
                
                # Read all sheets using pandas
                sheets_dict = pd.read_excel(
                    tmp_file.name,
                    sheet_name=None,  # Read all sheets
                    engine='openpyxl' if uploaded_file.name.endswith('.xlsx') else 'xlrd'
                )
                
                # Clean up temporary file
                Path(tmp_file.name).unlink()
                
                return sheets_dict
                
        except Exception as e:
            raise Exception(f"Error reading Excel sheets: {str(e)}")
    
    def get_sheet_preview(self, uploaded_file: UploadedFile, sheet_name: str, max_rows: int = 10) -> pd.DataFrame:
        """
        Get a preview of a specific sheet
        
        Args:
            uploaded_file: Streamlit uploaded file object
            sheet_name: Name of the sheet to preview
            max_rows: Maximum number of rows to return
            
        Returns:
            DataFrame with preview data
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.flush()
                
                # Read specific sheet with row limit
                df = pd.read_excel(
                    tmp_file.name,
                    sheet_name=sheet_name,
                    nrows=max_rows,
                    engine='openpyxl' if uploaded_file.name.endswith('.xlsx') else 'xlrd'
                )
                
                # Clean up temporary file
                Path(tmp_file.name).unlink()
                
                return df
                
        except Exception as e:
            raise Exception(f"Error reading sheet preview: {str(e)}")
    
    def save_uploaded_file_temporarily(self, uploaded_file: UploadedFile) -> str:
        """
        Save uploaded file to a temporary location for processing
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Path to the temporary file
        """
        try:
            # Create temporary file with original extension
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.flush()
                return tmp_file.name
                
        except Exception as e:
            raise Exception(f"Error saving temporary file: {str(e)}")
    
    def analyze_sheet_structure(self, uploaded_file: UploadedFile, sheet_name: str) -> Dict[str, Any]:
        """
        Analyze the structure of a specific sheet
        
        Args:
            uploaded_file: Streamlit uploaded file object
            sheet_name: Name of the sheet to analyze
            
        Returns:
            Dictionary with sheet analysis
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.flush()
                
                # Read the sheet
                df = pd.read_excel(
                    tmp_file.name,
                    sheet_name=sheet_name,
                    engine='openpyxl' if uploaded_file.name.endswith('.xlsx') else 'xlrd'
                )
                
                # Clean up temporary file
                Path(tmp_file.name).unlink()
                
                # Analyze structure
                analysis = {
                    'sheet_name': sheet_name,
                    'total_rows': len(df),
                    'total_columns': len(df.columns),
                    'empty_rows': df.isnull().all(axis=1).sum(),
                    'empty_columns': df.isnull().all(axis=0).sum(),
                    'has_data': not df.empty,
                    'column_names': df.columns.tolist(),
                    'data_types': df.dtypes.to_dict()
                }
                
                return analysis
                
        except Exception as e:
            raise Exception(f"Error analyzing sheet structure: {str(e)}")
    
    def get_non_empty_sheets(self, uploaded_file: UploadedFile) -> List[str]:
        """
        Get list of non-empty sheet names
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            List of non-empty sheet names
        """
        try:
            sheets_data = self.read_excel_sheets(uploaded_file)
            non_empty_sheets = []
            
            for sheet_name, df in sheets_data.items():
                if not df.empty and not df.isnull().all().all():
                    non_empty_sheets.append(sheet_name)
            
            return non_empty_sheets
            
        except Exception as e:
            raise Exception(f"Error identifying non-empty sheets: {str(e)}")
    
    def validate_excel_format(self, uploaded_file: UploadedFile) -> Tuple[bool, str]:
        """
        Validate that the uploaded file is a valid Excel format
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check file extension
            file_ext = Path(uploaded_file.name).suffix.lower()
            if file_ext not in self.supported_formats:
                return False, f"Unsupported file format. Please upload {', '.join(self.supported_formats)} files only."
            
            # Try to read the file to verify it's a valid Excel file
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file.flush()
                    
                    # Attempt to read with pandas
                    pd.read_excel(
                        tmp_file.name,
                        sheet_name=None,
                        engine='openpyxl' if file_ext == '.xlsx' else 'xlrd'
                    )
                    
                    # Clean up temporary file
                    Path(tmp_file.name).unlink()
                    
            except Exception as read_error:
                return False, f"Invalid Excel file format: {str(read_error)}"
            
            return True, "Valid Excel file"
            
        except Exception as e:
            return False, f"Error validating file: {str(e)}"