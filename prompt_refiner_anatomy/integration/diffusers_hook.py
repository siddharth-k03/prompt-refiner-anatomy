"""
HuggingFace Diffusers integration for the Prompt Refiner Anatomy module.

This module provides seamless integration with Diffusers pipelines,
perfect for Google Colab environments.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from ..enhancer import PromptRefiner

logger = logging.getLogger(__name__)


class DiffusersWrapper:
    """
    Wrapper class that enhances any Diffusers pipeline with anatomical prompt refinement.
    
    Example usage in Google Colab:
    ```python
    from diffusers import StableDiffusionPipeline
    from prompt_refiner_anatomy.integration import DiffusersWrapper
    
    # Load your pipeline
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    
    # Wrap with anatomical enhancement
    enhanced_pipe = DiffusersWrapper(pipe)
    
    # Generate with simple prompts
    image = enhanced_pipe("heart", view_type="cross_section")
    ```
    """
    
    def __init__(self, pipeline, refiner: Optional[PromptRefiner] = None):
        """
        Initialize wrapper with a Diffusers pipeline.
        
        Args:
            pipeline: Any HuggingFace Diffusers pipeline
            refiner: Optional custom PromptRefiner instance
        """
        self.pipeline = pipeline
        self.refiner = refiner or PromptRefiner()
        
        # Store original pipeline attributes for pass-through
        self._original_call = pipeline.__call__
        
    def __call__(self, prompt: str, focus: Optional[str] = None, 
                 view_type: str = "standard", **kwargs) -> Any:
        """
        Generate images with enhanced anatomical prompts.
        
        Args:
            prompt: Simple anatomical term (e.g., "heart", "brain")
            focus: Enhancement focus ("education", "3d_modeling", "scientific")  
            view_type: View type ("standard", "cross_section", "system_overview")
            **kwargs: Additional arguments passed to the original pipeline
            
        Returns:
            Generated images from the pipeline
        """
        # Enhance the prompt
        enhanced = self.refiner.enhance(prompt, focus=focus, view_type=view_type)
        
        # Log the enhancement for debugging
        logger.info(f"Enhanced prompt: '{prompt}' -> '{enhanced['positive'][:100]}...'")
        
        # Use enhanced prompts
        kwargs['prompt'] = enhanced['positive']
        if 'negative_prompt' not in kwargs:
            kwargs['negative_prompt'] = enhanced['negative']
        
        # Call original pipeline with enhanced prompts
        return self._original_call(**kwargs)
    
    def generate_batch(self, prompts: List[str], **kwargs) -> List[Any]:
        """
        Generate multiple images with enhanced prompts.
        
        Args:
            prompts: List of anatomical terms
            **kwargs: Arguments passed to each generation call
            
        Returns:
            List of generated image results
        """
        results = []
        for prompt in prompts:
            try:
                result = self(prompt, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to generate for prompt '{prompt}': {e}")
                results.append(None)
        
        return results
    
    def __getattr__(self, name):
        """Pass through all other attributes to the original pipeline."""
        return getattr(self.pipeline, name)


def enhance_pipeline(pipeline, refiner: Optional[PromptRefiner] = None) -> DiffusersWrapper:
    """
    Convenience function to enhance any Diffusers pipeline.
    
    Args:
        pipeline: HuggingFace Diffusers pipeline
        refiner: Optional custom PromptRefiner instance
        
    Returns:
        Enhanced pipeline with anatomical prompt refinement
        
    Example:
    ```python
    from diffusers import StableDiffusionPipeline
    from prompt_refiner_anatomy.integration import enhance_pipeline
    
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    enhanced_pipe = enhance_pipeline(pipe)
    
    # Now you can use simple anatomical terms
    image = enhanced_pipe("heart")
    ```
    """
    return DiffusersWrapper(pipeline, refiner)


def create_educational_pipeline(model_id: str = "runwayml/stable-diffusion-v1-5", 
                               device: str = "cuda", 
                               torch_dtype = None) -> DiffusersWrapper:
    """
    Create a pre-configured pipeline optimized for educational anatomical content.
    
    Args:
        model_id: HuggingFace model ID
        device: Device to run on ("cuda", "cpu", "mps")
        torch_dtype: Torch data type (e.g., torch.float16)
        
    Returns:
        Ready-to-use enhanced pipeline
        
    Example for Google Colab:
    ```python
    from prompt_refiner_anatomy.integration import create_educational_pipeline
    import torch
    
    pipe = create_educational_pipeline(
        device="cuda",
        torch_dtype=torch.float16  # Memory optimization
    )
    
    image = pipe("heart", focus="education")
    ```
    """
    try:
        from diffusers import StableDiffusionPipeline
        import torch
        
        # Set default dtype for memory efficiency
        if torch_dtype is None and device == "cuda":
            torch_dtype = torch.float16
        
        # Load pipeline
        pipeline = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            safety_checker=None,  # Disable for educational content
            requires_safety_checker=False
        )
        
        if device == "cuda" and torch.cuda.is_available():
            pipeline = pipeline.to(device)
            # Enable memory efficient attention if available
            try:
                pipeline.enable_xformers_memory_efficient_attention()
            except ImportError:
                logger.info("xformers not available, using default attention")
        
        # Wrap with anatomical enhancement
        return DiffusersWrapper(pipeline)
        
    except ImportError as e:
        raise ImportError(
            "This function requires diffusers and torch. "
            "Install with: pip install 'prompt-refiner-anatomy[colab]'"
        ) from e