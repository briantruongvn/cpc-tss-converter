"""Pipeline orchestrator — used by test scripts and CLI runners."""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from streamlit.runtime.uploaded_file_manager import UploadedFile

from .config_manager import ConfigManager
from .step1 import CoreTemplateCreator
from .step2 import CoreStep2Processor
from .step3 import CoreStep3DataTransfer
from .step4 import CoreStep4DuplicateRemover


class CorePipeline:
    """Unified pipeline orchestrator — used by test scripts and CLI runners"""

    def __init__(self, output_dir: Optional[str] = None, config_dir: Optional[str] = None):
        self.output_dir = output_dir
        self.config_dir = config_dir
        self.template_creator = CoreTemplateCreator(output_dir, config_dir)
        self.step2_processor = CoreStep2Processor(output_dir, config_dir)
        self.step3_processor = CoreStep3DataTransfer(output_dir, config_dir)
        self.step4_processor = CoreStep4DuplicateRemover(output_dir, config_dir)

    def process_complete_pipeline(
        self, source_file, sheet_names: List[str]
    ) -> Dict[str, Any]:
        """Run the complete pipeline for multiple sheets."""
        results: Dict[str, Any] = {
            'success_count': 0,
            'failed_count': 0,
            'step4_files': [],
            'failed_sheets': [],
            'total_sheets': len(sheet_names)
        }

        original_filename = (
            Path(source_file).name if isinstance(source_file, str) else source_file.name
        )

        for sheet_name in sheet_names:
            try:
                template_path = self.template_creator.create_template(sheet_name, original_filename)
                if not template_path:
                    raise Exception("Failed to create template")

                if isinstance(source_file, UploadedFile):
                    article_name, article_number = (
                        self.step2_processor.extract_article_info_from_uploaded_file(
                            source_file, sheet_name
                        )
                    )
                else:
                    article_name, article_number = (
                        self.step2_processor.extract_article_info_from_file(
                            source_file, sheet_name
                        )
                    )

                step2_path = self.step2_processor.populate_template_with_article_info(
                    template_path, article_name, article_number
                )
                step3_path = self.step3_processor.transfer_data(step2_path, source_file, sheet_name)
                step4_path = self.step4_processor.remove_duplicates(step3_path)

                results['success_count'] += 1
                results['step4_files'].append({
                    'sheet_name': sheet_name,
                    'filename': Path(step4_path).name,
                    'file_path': step4_path
                })

            except Exception as e:
                logging.error(f"Pipeline failed for sheet '{sheet_name}': {str(e)}")
                results['failed_count'] += 1
                results['failed_sheets'].append(sheet_name)

        return results

    def reload_configuration(self):
        """Reload all configurations."""
        ConfigManager.reload_configs()
        self.template_creator = CoreTemplateCreator(self.output_dir, self.config_dir)
        self.step2_processor = CoreStep2Processor(self.output_dir, self.config_dir)
        self.step3_processor = CoreStep3DataTransfer(self.output_dir, self.config_dir)
        self.step4_processor = CoreStep4DuplicateRemover(self.output_dir, self.config_dir)
