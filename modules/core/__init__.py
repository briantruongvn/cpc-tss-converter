"""
modules.core — Core business logic for the TSS pipeline.

Each module contains one class:
  config_manager  →  ConfigManager
  step1           →  CoreTemplateCreator
  step2           →  CoreStep2Processor
  step3           →  CoreStep3DataTransfer
  step4           →  CoreStep4DuplicateRemover
  pipeline        →  CorePipeline  (orchestrates all steps)
"""

from .config_manager import ConfigManager
from .step1 import CoreTemplateCreator
from .step2 import CoreStep2Processor
from .step3 import CoreStep3DataTransfer
from .step4 import CoreStep4DuplicateRemover
from .pipeline import CorePipeline

__all__ = [
    "ConfigManager",
    "CoreTemplateCreator",
    "CoreStep2Processor",
    "CoreStep3DataTransfer",
    "CoreStep4DuplicateRemover",
    "CorePipeline",
]
