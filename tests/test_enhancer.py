"""
Tests for the PromptRefiner class.
"""

import json
import pytest
from pathlib import Path

from prompt_refiner_anatomy import PromptRefiner
from prompt_refiner_anatomy.filters import SafetyFilter, EducationalFilter


class TestPromptRefiner:
    """Test cases for PromptRefiner functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.refiner = PromptRefiner()
    
    def test_initialization(self):
        """Test that PromptRefiner initializes correctly."""
        assert self.refiner is not None
        assert hasattr(self.refiner, 'data')
        assert 'body_systems' in self.refiner.data
    
    def test_enhance_heart(self):
        """Test enhancement of 'heart' prompt."""
        result = self.refiner.enhance("heart")
        
        assert isinstance(result, dict)
        assert 'positive' in result
        assert 'negative' in result
        assert 'detected_terms' in result
        assert 'detected_systems' in result
        
        # Check that heart was detected
        assert 'heart' in result['detected_terms']
        assert 'circulatory' in result['detected_systems']
        
        # Check that enhancement includes educational context
        positive = result['positive']
        assert 'anatomical illustration' in positive.lower()
        assert 'educational' in positive.lower()
        
        # Check negative prompt excludes inappropriate content
        negative = result['negative']
        assert 'blood' in negative
        assert 'gore' in negative
        assert 'labels' in negative
    
    def test_enhance_brain(self):
        """Test enhancement of 'brain' prompt."""
        result = self.refiner.enhance("brain")
        
        assert 'brain' in result['detected_terms']
        assert 'nervous' in result['detected_systems']
        assert 'anatomical illustration' in result['positive'].lower()
    
    def test_enhance_with_view_type(self):
        """Test enhancement with different view types."""
        # Test cross-section view
        result_cross = self.refiner.enhance("heart", view_type="cross_section")
        assert 'cross-section' in result_cross['positive'].lower()
        
        # Test system overview
        result_system = self.refiner.enhance("heart", view_type="system_overview")
        assert 'system' in result_system['positive'].lower()
    
    def test_enhance_with_focus(self):
        """Test enhancement with different focus areas."""
        # Test education focus
        result_edu = self.refiner.enhance("heart", focus="education")
        negative_edu = result_edu['negative']
        assert 'frightening' in negative_edu
        
        # Test 3D reconstruction focus
        result_3d = self.refiner.enhance("heart", focus="3d_reconstruction")
        negative_3d = result_3d['negative']
        assert 'multiple objects' in negative_3d
    
    def test_unknown_term(self):
        """Test enhancement of unknown anatomical term."""
        result = self.refiner.enhance("flibberjib")
        
        # Should still produce a result with fallback content
        assert 'positive' in result
        assert 'negative' in result
        assert len(result['detected_terms']) == 0
        assert len(result['detected_systems']) == 0
        
        # Should include general anatomical context
        positive = result['positive']
        assert 'anatomical' in positive.lower()
    
    def test_list_supported_terms(self):
        """Test listing of supported terms."""
        terms = self.refiner.list_supported_terms()
        
        assert isinstance(terms, dict)
        assert 'circulatory' in terms
        assert 'nervous' in terms
        assert 'skeletal' in terms
        
        # Check that heart is in circulatory terms
        assert 'heart' in terms['circulatory']
        assert 'brain' in terms['nervous']
    
    def test_get_system_info(self):
        """Test getting body system information."""
        heart_system = self.refiner.get_system_info('circulatory')
        
        assert heart_system is not None
        assert 'description' in heart_system
        assert 'organs' in heart_system
        assert 'heart' in heart_system['organs']
        
        # Test unknown system
        unknown_system = self.refiner.get_system_info('unknown')
        assert unknown_system is None


class TestSafetyFilter:
    """Test cases for SafetyFilter."""
    
    def setup_method(self):
        """Set up test fixtures."""
        forbidden_terms = ["blood", "gore", "surgical", "nude"]
        self.filter = SafetyFilter(forbidden_terms)
    
    def test_clean_prompt_removes_forbidden_terms(self):
        """Test that forbidden terms are removed."""
        dirty_prompt = "heart with blood and gore"
        cleaned = self.filter.clean_prompt(dirty_prompt)
        
        assert 'blood' not in cleaned
        assert 'gore' not in cleaned
        assert 'heart' in cleaned
    
    def test_clean_prompt_replaces_advanced_terms(self):
        """Test that advanced medical terms are replaced."""
        advanced_prompt = "surgical dissection of heart"
        cleaned = self.filter.clean_prompt(advanced_prompt)
        
        # Forbidden terms should be removed entirely
        assert 'surgical' not in cleaned
        assert 'dissection' not in cleaned
        # Advanced terms should be replaced by SafetyFilter.advanced_medical
        assert 'diagram' in cleaned  # replacement for dissection
        assert 'heart' in cleaned  # original anatomical term preserved
    
    def test_is_safe(self):
        """Test safety checking."""
        assert self.filter.is_safe("heart anatomy") is True
        assert self.filter.is_safe("heart with blood") is False
        assert self.filter.is_safe("nude anatomy") is False


class TestEducationalFilter:
    """Test cases for EducationalFilter."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Load body systems data
        data_path = Path(__file__).parent.parent / "prompt_refiner_anatomy" / "data" / "anatomical_terms.json"
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        self.filter = EducationalFilter(data['body_systems'])
    
    def test_ensure_appropriate_adds_context(self):
        """Test that educational context is added when missing."""
        basic_prompt = "heart diagram"
        enhanced = self.filter.ensure_appropriate(basic_prompt)
        
        # Should contain educational indicators (already has 'diagram' so may not add more)
        # The filter checks for educational context and adds if missing
        assert 'diagram' in enhanced.lower()  # Basic check
        
        # Test with non-educational prompt
        non_edu_prompt = "heart muscle tissue"
        enhanced_non_edu = self.filter.ensure_appropriate(non_edu_prompt)
        assert any(indicator in enhanced_non_edu.lower() for indicator in ['educational', 'science', 'elementary'])
    
    def test_contains_valid_anatomy(self):
        """Test anatomical term detection."""
        assert self.filter._contains_valid_anatomy("heart diagram") is True
        assert self.filter._contains_valid_anatomy("random stuff") is False
    
    def test_validate_system_focus(self):
        """Test body system focus validation."""
        assert self.filter.validate_system_focus("heart pump", "circulatory") is True
        assert self.filter.validate_system_focus("brain thinking", "nervous") is True
        assert self.filter.validate_system_focus("heart pump", "skeletal") is False


if __name__ == "__main__":
    pytest.main([__file__])