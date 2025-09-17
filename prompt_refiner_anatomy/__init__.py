"""
Prompt Refiner for Anatomical Education

A plug-and-play module for enhancing text prompts in Stable Diffusion
to generate educational anatomical content suitable for 3D modeling.

Designed for K-6 grade school education with safety-first approach.
"""

__version__ = "0.1.0"
__author__ = "Educational AI Tools"
__license__ = "MIT"

from .enhancer import PromptRefiner
from .filters import SafetyFilter, EducationalFilter

__all__ = ["PromptRefiner", "SafetyFilter", "EducationalFilter"]