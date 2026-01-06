#!/usr/bin/env python3
"""
Step 1: Create Initial Template
Creates structured output template for Excel format conversion.
Uses CoreTemplateCreator for unified business logic.
"""

import logging
from pathlib import Path
from typing import Union, Optional
import argparse
import sys

# Import core pipeline for unified logic
from modules.core_pipeline import CoreTemplateCreator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TemplateCreator:
    """
    Local Template Creator for Step 1
    
    Wrapper around CoreTemplateCreator for local file processing.
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        # Set up base directory
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(".")
        
        # Set up output directory
        output_dir = self.base_dir / "output"
        
        # Initialize core template creator
        self.core_creator = CoreTemplateCreator(str(output_dir))
    
    def create_template(self, input_file: Union[str, Path], 
                       output_file: Optional[Union[str, Path]] = None) -> str:
        """
        Create output template from input Excel file
        
        Args:
            input_file: Input Excel file (.xlsx)
            output_file: Optional output file path (if None, auto-generate)
            
        Returns:
            Path to template file
        """
        logger.info("📋 Step 1: Create Initial Template")
        
        # Validate input file format
        input_path = Path(input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if input_path.suffix.lower() not in ['.xlsx', '.xls']:
            raise ValueError(f"Invalid file format. Expected .xlsx or .xls, got {input_path.suffix}")
        
        logger.info(f"Input: {input_path}")
        
        # For local processing, we create a template for the main file
        # Extract filename for template creation
        filename = input_path.name
        sheet_name = "Template"  # Default sheet name for local processing
        
        # Use core creator to create template
        template_path = self.core_creator.create_template(sheet_name, filename)
        
        # If custom output path specified, rename the file
        if output_file:
            output_path = Path(output_file)
            if template_path:
                Path(template_path).rename(output_path)
                template_path = str(output_path)
                logger.info(f"Template saved to custom path: {output_path}")
        
        if template_path:
            logger.info(f"✅ Step 1 completed: {template_path}")
            
            # Validate template structure
            if self.core_creator.validate_template_structure(template_path):
                logger.info("✅ Template validation passed")
            else:
                logger.warning("⚠️ Template validation failed")
        else:
            raise RuntimeError("Failed to create template")
        
        return template_path
    
    def create_multiple_templates(self, input_patterns: list, output_dir: Optional[str] = None) -> list:
        """
        Create templates for multiple files matching patterns
        
        Args:
            input_patterns: List of file patterns or paths
            output_dir: Output directory (if None, use default)
            
        Returns:
            List of output file paths
        """
        if output_dir:
            # Update core creator with new output directory
            self.core_creator = CoreTemplateCreator(str(Path(output_dir)))
        
        results = []
        
        for pattern in input_patterns:
            # Handle glob patterns
            if '*' in str(pattern):
                input_files = list(self.base_dir.glob(str(pattern)))
            else:
                input_files = [Path(pattern)]
            
            for input_file in input_files:
                if input_file.exists() and input_file.suffix.lower() in ['.xlsx', '.xls']:
                    try:
                        result = self.create_template(input_file)
                        results.append(result)
                        logger.info(f"✅ Processed: {input_file} → {result}")
                    except Exception as e:
                        logger.error(f"❌ Failed to process {input_file}: {e}")
                else:
                    logger.warning(f"⚠️  Skipped: {input_file} (not found or not Excel file)")
        
        return results

def main():
    """Command line interface for standalone template creation"""
    parser = argparse.ArgumentParser(description='Template Creator Step 1 - Initial Template Creation')
    parser.add_argument('input', nargs='+', help='Input Excel file(s) (.xlsx format)')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('-d', '--base-dir', help='Base directory', default='.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose logging')
    parser.add_argument('--batch', action='store_true', help='Batch mode for multiple files')
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize creator
    creator = TemplateCreator(args.base_dir)
    
    try:
        if args.batch or len(args.input) > 1:
            # Multiple files mode
            output_dir = args.output if args.output else None
            results = creator.create_multiple_templates(args.input, output_dir)
            
            print("\n📊 Batch Processing Results:")
            print(f"✅ Successfully processed: {len(results)} files")
            for result in results:
                print(f"   📁 {result}")
                
        else:
            # Single file mode
            input_file = args.input[0]
            output_file = args.output
            
            result = creator.create_template(input_file, output_file)
            print(f"\n✅ Success!")
            print(f"📁 Output: {result}")
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()