# Release Notes v0.1.0 - Initial Release

## 🎉 First Release: Prompt Refiner for Anatomical Education

A plug-and-play Python module that enhances text prompts for Stable Diffusion to generate educational anatomical content suitable for 3D modeling and K-6 grade education.

### ✨ Key Features

- **Smart Prompt Enhancement**: Automatically detects anatomical terms and adds educational context
- **Safety Filters**: Blocks inappropriate medical content for K-6 safety standards  
- **3D-Optimized Output**: Adds tags like "orthographic view, clean topology" for better 3D modeling
- **Label-Free Generation**: Avoids text/annotations that don't generate well in SD
- **Google Colab Ready**: Seamless integration with Diffusers pipelines
- **CLI Interface**: Easy PowerShell/command-line usage for Windows users
- **Zero External Dependencies**: Pure Python for maximum compatibility

### 🧠 Anatomical Coverage

- **6 Body Systems**: Skeletal, Circulatory, Respiratory, Nervous, Digestive, Muscular
- **60+ Terms**: Comprehensive K-6 appropriate vocabulary
- **Multiple Views**: Standard, cross-section, system overview
- **Focus Modes**: Education, 3D modeling, scientific

### 🚀 Quick Start

```bash
# Install
pip install prompt-refiner-anatomy

# Basic usage
python -m prompt_refiner_anatomy "heart"

# For Google Colab
pip install prompt-refiner-anatomy[colab]
```

### 📋 Example Output

**Input**: `"heart"`  
**Enhanced**: `"anatomical illustration of heart, medical textbook style, educational diagram, for grade school science class, orthographic projection, clean topology, neutral lighting"`  
**Negative**: `"blood, gore, graphic, text, labels, annotations, arrows, numbers"`

### 🎯 Perfect For

- **Educators**: Creating anatomical reference images for science classes
- **3D Modelers**: Generating clean reference imagery without labels
- **Students**: Learning anatomy through visual aids
- **Google Colab Users**: GPU-accelerated generation in the cloud

### 🛠️ Technical Details

- **Python 3.8+ compatibility**
- **Comprehensive test suite** (14 tests)
- **MIT License** with CC-BY-SA vocabulary database
- **Professional packaging** with setuptools
- **Cross-platform support** (Windows, macOS, Linux)

### 📦 Installation Options

```bash
# Core functionality only
pip install prompt-refiner-anatomy

# With Google Colab dependencies
pip install prompt-refiner-anatomy[colab]

# Development dependencies
pip install prompt-refiner-anatomy[dev]
```

### 🔧 CLI Examples

```powershell
# List all supported terms
python -m prompt_refiner_anatomy --list-terms

# Generate 3D-optimized prompts
python -m prompt_refiner_anatomy "brain" --view-type cross_section --focus 3d_modeling

# JSON output for automation
python -m prompt_refiner_anatomy "skeleton" --output json
```

### 📚 Documentation

- **README.md**: Complete usage guide with examples
- **PowerShell Demo**: `examples/demo_ps.ps1` generates sample prompts
- **Test Suite**: Comprehensive validation of all features
- **Type Hints**: Full typing support for development

### 🙏 Educational Focus

This tool is specifically designed for **K-6 educational content** with:
- Age-appropriate anatomical terminology
- Simplified, clean illustrations  
- No graphic medical content
- Educational context built into every prompt
- Perfect for science class presentations

---

**Made for educators, by educators** 🍎

Perfect for creating anatomical reference images for science classes, 3D modeling projects, and educational materials. Safe, simple, and effective.

### Files in this release:
- `prompt_refiner_anatomy-0.1.0-py3-none-any.whl` - Wheel distribution
- `prompt_refiner_anatomy-0.1.0.tar.gz` - Source distribution