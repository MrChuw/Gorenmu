"""Top-level package for Deep Translator"""

__copyright__ = "Copyright (C) 2020 Nidhal Baccouri"

from .detection import batch_detection, single_detection
from .google import GoogleTranslator

__author__ = """Nidhal Baccouri"""
__email__ = "nidhalbacc@gmail.com"
__version__ = "1.9.1"

__all__ = [
    "GoogleTranslator",
    "single_detection",
    "batch_detection",
]
