"""
Google Colab utilities for easy setup and model management.

This module provides helper functions specifically designed for Google Colab
environments to make anatomical content generation as smooth as possible.
"""

import logging
import os
import subprocess
import sys
from typing import Optional

logger = logging.getLogger(__name__)


def setup_colab_environment(install_dependencies: bool = True, 
                           enable_gpu: bool = True) -> None:
    """
    Set up Google Colab environment for anatomical content generation.
    
    Args:
        install_dependencies: Whether to install required packages
        enable_gpu: Whether to check and configure GPU support
        
    Example usage in Colab:
    ```python
    from prompt_refiner_anatomy.integration import setup_colab_environment
    
    # One-line setup
    setup_colab_environment()
    ```
    """
    print("🔧 Setting up Colab environment for anatomical content generation...")
    
    # Check if running in Colab
    try:
        import google.colab
        print("✅ Google Colab environment detected")
    except ImportError:
        print("⚠️  Not running in Google Colab, skipping Colab-specific setup")
        return
    
    if install_dependencies:
        print("📦 Installing dependencies...")
        _install_colab_dependencies()
    
    if enable_gpu:
        _check_gpu_setup()
    
    # Set up logging for better debugging
    logging.basicConfig(level=logging.INFO, 
                       format='%(levelname)s: %(message)s')
    
    print("🎉 Colab environment setup complete!")
    print("💡 You can now use: from prompt_refiner_anatomy.integration import create_educational_pipeline")


def _install_colab_dependencies():
    """Install required packages for Colab."""
    packages = [
        "diffusers>=0.21.0",
        "transformers>=4.25.0", 
        "accelerate>=0.20.0",
        "safetensors>=0.3.0"
    ]
    
    for package in packages:
        try:
            print(f"  Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to install {package}: {e}")


def _check_gpu_setup():
    """Check GPU availability and configuration."""
    print("🎮 Checking GPU setup...")
    
    try:
        import torch
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✅ GPU available: {gpu_name} ({gpu_memory:.1f}GB)")
            
            # Recommend settings based on GPU
            if gpu_memory < 8:
                print("⚠️  Low GPU memory detected. Consider using torch.float16 for memory efficiency")
            else:
                print("✅ Sufficient GPU memory for standard generation")
                
        else:
            print("❌ No GPU available. Generation will be slow on CPU")
            
    except ImportError:
        print("⚠️  PyTorch not installed, cannot check GPU status")


def download_models(model_ids: list = None, cache_dir: str = "/tmp/huggingface_cache") -> None:
    """
    Pre-download models to avoid timeout issues during generation.
    
    Args:
        model_ids: List of model IDs to download. Defaults to common models.
        cache_dir: Directory to cache models
        
    Example:
    ```python
    from prompt_refiner_anatomy.integration import download_models
    
    # Download common models
    download_models()
    ```
    """
    if model_ids is None:
        model_ids = [
            "runwayml/stable-diffusion-v1-5",
            # Add more common models here
        ]
    
    print(f"📥 Pre-downloading models to {cache_dir}...")
    
    try:
        from huggingface_hub import snapshot_download
        
        for model_id in model_ids:
            print(f"  Downloading {model_id}...")
            try:
                snapshot_download(
                    repo_id=model_id,
                    cache_dir=cache_dir,
                    ignore_patterns=["*.bin"]  # Skip large files for now
                )
                print(f"  ✅ {model_id} cached")
            except Exception as e:
                logger.warning(f"Failed to cache {model_id}: {e}")
                
    except ImportError:
        logger.warning("huggingface_hub not available, skipping model pre-download")


def get_colab_code_snippet() -> str:
    """
    Get a ready-to-use code snippet for Colab notebooks.
    
    Returns:
        Python code string ready to paste into Colab
    """
    return '''
# Install and setup prompt refiner for anatomical content
!pip install prompt-refiner-anatomy[colab]

# Setup environment
from prompt_refiner_anatomy.integration import setup_colab_environment, create_educational_pipeline
setup_colab_environment()

# Create enhanced pipeline
import torch
pipe = create_educational_pipeline(
    device="cuda" if torch.cuda.is_available() else "cpu",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

# Generate anatomical content
image = pipe("heart", focus="education", view_type="cross_section")
image.images[0].show()

# Try different organs
for organ in ["brain", "lungs", "skeleton"]:
    print(f"\\nGenerating {organ}...")
    result = pipe(organ, focus="3d_modeling")
    result.images[0].show()
'''


def create_colab_demo() -> str:
    """
    Create a complete Colab demo notebook content.
    
    Returns:
        Markdown and code content for a Colab notebook
    """
    return '''
# Anatomical Content Generation for Education

This notebook demonstrates how to generate educational anatomical content using Stable Diffusion with the Prompt Refiner Anatomy module.

## Setup

''' + get_colab_code_snippet() + '''

## Advanced Usage

```python
# Batch generation
organs = ["heart", "brain", "lungs", "liver", "kidneys"]
results = pipe.generate_batch(organs, focus="education", num_inference_steps=20)

# Display all results
for i, (organ, result) in enumerate(zip(organs, results)):
    if result:
        print(f"{organ.title()}:")
        result.images[0].show()
```

## 3D Modeling Optimization

```python
# Generate content optimized for 3D model creation
organs_3d = ["skull", "spine", "pelvis", "femur"]

for organ in organs_3d:
    print(f"\\nGenerating {organ} for 3D modeling...")
    result = pipe(
        organ, 
        focus="3d_modeling", 
        view_type="cross_section",
        guidance_scale=7.5,
        num_inference_steps=30
    )
    result.images[0].show()
```
'''