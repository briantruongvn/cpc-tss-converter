#!/usr/bin/env python3
"""
Local Pipeline Test Script
Test the complete pipeline with rotation and merged cells fix
"""

import logging
import sys
from pathlib import Path

# Import core pipeline
from modules.core_pipeline import CorePipeline

# Configure logging with DEBUG level to see all rotation/merge logs
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run local pipeline test"""
    logger.info("🚀 Starting Local Pipeline Test")
    
    # Set up paths
    base_dir = Path("/Users/truongxuantruong/Desktop/CPC Internal TSS Converter")
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"
    
    # Find input Excel file
    input_files = list(input_dir.glob("*.xlsx"))
    if not input_files:
        logger.error("❌ No Excel files found in input directory")
        sys.exit(1)
    
    input_file = input_files[0]
    logger.info(f"📁 Input file: {input_file.name}")
    
    # Initialize pipeline
    pipeline = CorePipeline(
        output_dir=str(output_dir),
        config_dir=str(base_dir / "config")
    )
    
    # Get sheet names from input file
    import pandas as pd
    xls = pd.ExcelFile(input_file)
    sheet_names = xls.sheet_names
    logger.info(f"📋 Found {len(sheet_names)} sheets: {sheet_names}")
    
    # Process all sheets
    test_sheets = sheet_names
    logger.info(f"🎯 Processing all sheets: {test_sheets}")
    
    # Run complete pipeline
    logger.info("🔄 Running complete pipeline...")
    results = pipeline.process_complete_pipeline(
        source_file=str(input_file),
        sheet_names=test_sheets
    )
    
    # Display results
    logger.info("=" * 50)
    logger.info("📊 PIPELINE RESULTS:")
    logger.info(f"✅ Success: {results['success_count']}/{results['total_sheets']} sheets")
    logger.info(f"❌ Failed: {results['failed_count']}/{results['total_sheets']} sheets")
    
    if results['step4_files']:
        logger.info("📁 Generated Step 4 files:")
        for file_info in results['step4_files']:
            logger.info(f"   - {file_info['filename']}")
    
    if results['failed_sheets']:
        logger.warning(f"⚠️ Failed sheets: {results['failed_sheets']}")
    
    logger.info("=" * 50)
    logger.info("🎉 Pipeline test completed!")
    
    # Instructions for manual verification
    logger.info("📋 Manual Verification Steps:")
    logger.info("1. Open the Step 4 files in Excel")
    logger.info("2. Check if column R1 has merged cells (R1:R9)")
    logger.info("3. Check if column R1 has 90° rotation")
    logger.info("4. Check if all data rows preserve formatting")

if __name__ == "__main__":
    main()