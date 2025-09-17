"""
Integration adapters for different Stable Diffusion implementations.

This module provides easy integration with popular SD frameworks:
- HuggingFace Diffusers (for Google Colab)  
- Automatic1111 WebUI
- ComfyUI (future)
"""

from .diffusers_hook import enhance_pipeline, DiffusersWrapper
from .colab_utils import setup_colab_environment, download_models

__all__ = [
    "enhance_pipeline", 
    "DiffusersWrapper",
    "setup_colab_environment",
    "download_models"
]