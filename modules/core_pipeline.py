"""
Backwards-compatibility shim.

Business logic has been split into modules/core/:
  config_manager.py  →  ConfigManager
  step1.py           →  CoreTemplateCreator
  step2.py           →  CoreStep2Processor
  step3.py           →  CoreStep3DataTransfer
  step4.py           →  CoreStep4DuplicateRemover
  pipeline.py        →  CorePipeline

Import directly from modules.core for new code.
"""

from .core import *  # noqa: F401, F403
