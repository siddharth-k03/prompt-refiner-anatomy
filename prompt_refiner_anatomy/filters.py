"""
Safety and educational appropriateness filters for anatomical content.
"""

import re
import logging
from typing import Dict, List, Set

logger = logging.getLogger(__name__)


class SafetyFilter:
    """
    Content safety filter to ensure age-appropriate anatomical content.
    
    Blocks inappropriate medical content and ensures K-6 safety standards.
    """
    
    def __init__(self, forbidden_terms: List[str]):
        """
        Initialize safety filter with forbidden terms.
        
        Args:
            forbidden_terms: List of terms to block or replace
        """
        self.forbidden_terms = set(term.lower() for term in forbidden_terms)
        
        # Common NSFW patterns to catch
        self.nsfw_patterns = [
            r'\b(nude?|naked|undressed)\b',
            r'\b(sexual?|erotic|arousal)\b',
            r'\b(genital|penis|vagina|breast)\b',
            r'\b(reproductive|fertility|conception)\b'
        ]
        
        # Medical terms that are too advanced/graphic for K-6
        self.advanced_medical = {
            'dissection': 'diagram',
            'autopsy': 'study',
            'cadaver': 'model',
            'surgical': 'medical',
            'pathology': 'health study',
            'trauma': 'injury study',
            'blood': 'circulation',
            'gore': 'anatomy'
        }
    
    def clean_prompt(self, prompt: str) -> str:
        """
        Clean the input prompt by removing/replacing inappropriate content.
        
        Args:
            prompt: Original user prompt
            
        Returns:
            Cleaned prompt safe for K-6 education
        """
        cleaned = prompt.lower().strip()
        
        # Check for forbidden terms and replace
        for term in self.forbidden_terms:
            if term in cleaned:
                logger.warning(f"Blocked forbidden term: {term}")
                # Remove the term entirely
                cleaned = re.sub(r'\b' + re.escape(term) + r'\b', '', cleaned, flags=re.IGNORECASE)
        
        # Replace advanced medical terms with K-6 appropriate alternatives
        for advanced_term, replacement in self.advanced_medical.items():
            cleaned = re.sub(r'\b' + re.escape(advanced_term) + r'\b', 
                           replacement, cleaned, flags=re.IGNORECASE)
        
        # Check NSFW patterns
        for pattern in self.nsfw_patterns:
            if re.search(pattern, cleaned, re.IGNORECASE):
                logger.warning(f"Blocked NSFW content matching pattern: {pattern}")
                cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        if not cleaned:
            # If everything was filtered out, provide safe fallback
            logger.info("Prompt completely filtered, using safe fallback")
            cleaned = "human anatomy educational diagram"
        
        return cleaned
    
    def is_safe(self, prompt: str) -> bool:
        """
        Check if a prompt is safe for K-6 education.
        
        Args:
            prompt: Prompt to check
            
        Returns:
            True if safe, False otherwise
        """
        prompt_lower = prompt.lower()
        
        # Check forbidden terms
        for term in self.forbidden_terms:
            if term in prompt_lower:
                return False
        
        # Check NSFW patterns
        for pattern in self.nsfw_patterns:
            if re.search(pattern, prompt_lower, re.IGNORECASE):
                return False
        
        return True


class EducationalFilter:
    """
    Filter to ensure content is appropriate for educational use.
    
    Validates anatomical accuracy and age-appropriateness for K-6 students.
    """
    
    def __init__(self, body_systems: Dict):
        """
        Initialize educational filter with anatomical knowledge base.
        
        Args:
            body_systems: Dictionary of body systems and their components
        """
        self.body_systems = body_systems
        
        # Build comprehensive vocabulary of valid terms
        self.valid_terms = set()
        for system_data in body_systems.values():
            self.valid_terms.update(term.lower() for term in system_data["organs"])
            self.valid_terms.update(term.lower() for term in system_data["keywords"])
        
        # Educational quality indicators
        self.educational_indicators = {
            'positive': ['diagram', 'illustration', 'educational', 'learning', 'study', 
                        'science', 'anatomy', 'medical', 'textbook', 'simplified'],
            'negative': ['complex', 'advanced', 'professional', 'clinical', 'pathological']
        }
    
    def ensure_appropriate(self, prompt: str) -> str:
        """
        Ensure the prompt is educationally appropriate for K-6 students.
        
        Args:
            prompt: Enhanced prompt to validate
            
        Returns:
            Validated and potentially modified prompt
        """
        # Check if prompt contains at least one valid anatomical term
        if not self._contains_valid_anatomy(prompt):
            logger.warning("Prompt lacks valid anatomical content")
            prompt = f"human anatomy educational diagram, {prompt}"
        
        # Ensure educational context is present
        if not self._has_educational_context(prompt):
            logger.info("Adding educational context to prompt")
            prompt = f"{prompt}, educational illustration for elementary science"
        
        # Remove any accidentally included advanced terms
        prompt = self._simplify_language(prompt)
        
        return prompt
    
    def _contains_valid_anatomy(self, prompt: str) -> bool:
        """Check if prompt contains valid anatomical terms."""
        prompt_lower = prompt.lower()
        return any(term in prompt_lower for term in self.valid_terms)
    
    def _has_educational_context(self, prompt: str) -> bool:
        """Check if prompt has educational context markers."""
        prompt_lower = prompt.lower()
        return any(indicator in prompt_lower 
                  for indicator in self.educational_indicators['positive'])
    
    def _simplify_language(self, prompt: str) -> str:
        """Replace complex terms with simpler alternatives."""
        # Dictionary of complex -> simple replacements
        simplifications = {
            'anatomical structure': 'body part',
            'physiological': 'body function',
            'morphology': 'shape',
            'pathophysiology': 'how illness affects the body',
            'biomechanics': 'how the body moves',
            'histology': 'tissue study'
        }
        
        result = prompt
        for complex_term, simple_term in simplifications.items():
            result = re.sub(r'\b' + re.escape(complex_term) + r'\b', 
                          simple_term, result, flags=re.IGNORECASE)
        
        return result
    
    def validate_system_focus(self, prompt: str, system_name: str) -> bool:
        """
        Validate that prompt appropriately focuses on specified body system.
        
        Args:
            prompt: Prompt to validate
            system_name: Target body system name
            
        Returns:
            True if prompt appropriately focuses on the system
        """
        if system_name not in self.body_systems:
            return False
        
        system_data = self.body_systems[system_name]
        prompt_lower = prompt.lower()
        
        # Check if any system-specific terms are present
        system_terms = system_data["organs"] + system_data["keywords"]
        return any(term.lower() in prompt_lower for term in system_terms)
    
    def get_age_appropriate_description(self, system_name: str) -> str:
        """
        Get age-appropriate description for a body system.
        
        Args:
            system_name: Name of body system
            
        Returns:
            K-6 appropriate description
        """
        if system_name not in self.body_systems:
            return "body system that helps keep us healthy"
        
        return self.body_systems[system_name]["description"]