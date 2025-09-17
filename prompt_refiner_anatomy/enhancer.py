"""
Core prompt enhancement engine for anatomical education content.
"""

import json
import random
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from .filters import EducationalFilter, SafetyFilter


class PromptRefiner:
    """
    Main class for enhancing prompts to generate educational anatomical content.
    
    Focuses on creating clean, unlabeled anatomical illustrations suitable for
    3D modeling and K-6 grade education.
    """
    
    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize the PromptRefiner with anatomical vocabulary.
        
        Args:
            data_path: Path to anatomical_terms.json file. If None, uses bundled data.
        """
        if data_path is None:
            data_path = Path(__file__).parent / "data" / "anatomical_terms.json"
        
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.safety_filter = SafetyFilter(self.data["forbidden_terms"])
        self.educational_filter = EducationalFilter(self.data["body_systems"])
        
    def enhance(self, prompt: str, focus: Optional[str] = None, 
                view_type: str = "standard") -> Dict[str, str]:
        """
        Enhance a prompt for anatomical education content.
        
        Args:
            prompt: Original user prompt (e.g., "heart")
            focus: Optional focus area ("3d_modeling", "education", "scientific")
            view_type: Type of view ("standard", "cross_section", "system_overview")
            
        Returns:
            Dict with "positive" and "negative" prompt keys
        """
        # Safety check first
        cleaned_prompt = self.safety_filter.clean_prompt(prompt)
        
        # Detect anatomical terms and systems
        detected_terms = self._detect_anatomical_terms(cleaned_prompt)
        detected_systems = self._detect_body_systems(detected_terms)
        
        # Build enhanced positive prompt
        positive_prompt = self._build_positive_prompt(
            cleaned_prompt, detected_terms, detected_systems, view_type, focus
        )
        
        # Build negative prompt to avoid unwanted content
        negative_prompt = self._build_negative_prompt(focus)
        
        # Final educational appropriateness check
        positive_prompt = self.educational_filter.ensure_appropriate(positive_prompt)
        
        return {
            "positive": positive_prompt,
            "negative": negative_prompt,
            "detected_terms": detected_terms,
            "detected_systems": detected_systems
        }
    
    def _detect_anatomical_terms(self, prompt: str) -> List[str]:
        """Detect anatomical terms in the prompt."""
        detected = []
        prompt_lower = prompt.lower()
        
        # Check all organs across all systems
        for system_data in self.data["body_systems"].values():
            for organ in system_data["organs"]:
                if organ.lower() in prompt_lower:
                    detected.append(organ)
            
            # Also check anatomical structures
            for structure in system_data["structures"]:
                if structure.lower() in prompt_lower:
                    detected.append(structure)
        
        return list(set(detected))  # Remove duplicates
    
    def _detect_body_systems(self, detected_terms: List[str]) -> List[str]:
        """Determine which body systems are referenced."""
        systems = []
        
        for system_name, system_data in self.data["body_systems"].items():
            # Check if any detected terms belong to this system
            system_terms = system_data["organs"] + system_data["structures"]
            if any(term.lower() in [t.lower() for t in system_terms] for term in detected_terms):
                systems.append(system_name)
        
        return systems
    
    def _build_positive_prompt(self, original_prompt: str, detected_terms: List[str], 
                             detected_systems: List[str], view_type: str, focus: Optional[str] = None) -> str:
        """Build the enhanced positive prompt based on focus."""
        parts = []
        
        # Get primary organ/term
        primary_term = detected_terms[0] if detected_terms else original_prompt
        
        # Use focus-specific templates if focus is specified
        if focus and focus in self.data["focus_templates"]:
            focus_config = self.data["focus_templates"][focus]
            
            # Start with focus-specific style prefix
            parts.append(focus_config["style_prefix"].format(organ=primary_term))
            
            # Add focus-specific context
            parts.append(focus_config["context"])
            
            # Add view-specific modifiers
            if view_type == "cross_section" and detected_terms:
                cross_section_template = self.data["enhancement_templates"]["cross_section"]
                parts.append(cross_section_template.format(organ=detected_terms[0]))
            elif view_type == "system_overview" and detected_systems:
                system_template = self.data["enhancement_templates"]["system_overview"]
                parts.append(system_template.format(system=detected_systems[0]))
            
            # Add focus-specific style modifiers (select 2-3)
            style_modifiers = random.sample(focus_config["style_modifiers"], 
                                          min(3, len(focus_config["style_modifiers"])))
            parts.extend(style_modifiers)
            
            # Add focus-specific view modifier
            view_modifier = random.choice(focus_config["view_modifiers"])
            parts.append(view_modifier)
            
            # Add focus-specific optimization tags
            optimization_tags = random.sample(focus_config["optimization_tags"], 
                                            min(4, len(focus_config["optimization_tags"])))
            parts.extend(optimization_tags)
            
        else:
            # Default behavior (no focus specified)
            if detected_terms:
                base_template = self.data["enhancement_templates"]["medical_illustration"]
                parts.append(base_template.format(organ=primary_term))
            else:
                parts.append(f"anatomical illustration, {original_prompt}")
            
            # Add view-specific modifiers
            if view_type == "cross_section" and detected_terms:
                cross_section_template = self.data["enhancement_templates"]["cross_section"]
                parts.append(cross_section_template.format(organ=detected_terms[0]))
            elif view_type == "system_overview" and detected_systems:
                system_template = self.data["enhancement_templates"]["system_overview"]
                parts.append(system_template.format(system=detected_systems[0]))
            
            # Add educational context
            parts.append(self.data["enhancement_templates"]["educational_context"])
            
            # Add default style modifiers
            style_modifiers = random.sample(self.data["style_modifiers"], 
                                          min(2, len(self.data["style_modifiers"])))
            parts.extend(style_modifiers)
            
            # Add default view modifier
            view_modifier = random.choice(self.data["view_modifiers"])
            parts.append(view_modifier)
            
            # Add default 3D optimization tags
            optimization_tags = random.sample(self.data["3d_optimization_tags"], 3)
            parts.extend(optimization_tags)
        
        return ", ".join(parts)
    
    def _build_negative_prompt(self, focus: Optional[str] = None) -> str:
        """Build negative prompt to avoid unwanted content based on focus."""
        negative_parts = self.data["negative_prompt_additions"].copy()
        
        # Add focus-specific negative prompts
        if focus and focus in self.data["focus_negative_prompts"]:
            focus_negatives = self.data["focus_negative_prompts"][focus]
            negative_parts.extend(focus_negatives)
        
        return ", ".join(negative_parts)
    
    def get_system_info(self, system_name: str) -> Optional[Dict]:
        """Get information about a specific body system."""
        return self.data["body_systems"].get(system_name)
    
    def list_supported_terms(self) -> Dict[str, List[str]]:
        """Get all supported anatomical terms organized by system."""
        result = {}
        for system_name, system_data in self.data["body_systems"].items():
            result[system_name] = system_data["organs"] + system_data["structures"]
        return result
