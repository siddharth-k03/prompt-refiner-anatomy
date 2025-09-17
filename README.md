# Prompt Refiner for Anatomical Education

A plug-and-play Python module that enhances text prompts for Stable Diffusion to generate educational anatomical content suitable for 3D modeling and Grade School education.

🎯 **Perfect for educators** who want to generate clean, age-appropriate anatomical illustrations  
🔧 **Optimized for Google Colab** where most users run Stable Diffusion  
🎨 **No-label approach** - generates clean anatomical structures perfect for 3D model reference  
🛡️ **Safety-first** - Built-in content filtering for educational appropriateness  

## Features

- ✅ **Smart Prompt Enhancement** - Automatically detects anatomical terms and adds educational context
- ✅ **Safety Filters** - Blocks inappropriate medical content for K-6 safety standards  
- ✅ **3D-Optimized Output** - Adds tags like "orthographic view, clean topology" for better 3D modeling
- ✅ **Label-Free Generation** - Avoids text/annotations that don't generate well in SD
- ✅ **Google Colab Ready** - Seamless integration with Diffusers pipelines
- ✅ **CLI Interface** - Easy PowerShell/command-line usage for Windows users
- ✅ **Zero External Dependencies** - Pure Python for maximum compatibility

## Quick Start

### Installation

```bash
# Basic installation
pip install prompt-refiner-anatomy

# For Google Colab (includes diffusers, torch, etc.)
pip install prompt-refiner-anatomy[colab]
```

### Command Line Usage

```powershell
# Basic usage
python -m prompt_refiner_anatomy "heart"

# Cross-section view optimized for 3D modeling  
python -m prompt_refiner_anatomy "brain" --view-type cross_section --focus 3d_modeling

# Get JSON output for automation
python -m prompt_refiner_anatomy "skeleton" --output json

# List all supported anatomical terms
python -m prompt_refiner_anatomy --list-terms
```

### Google Colab Usage

```python
# Install in Colab
!pip install prompt-refiner-anatomy[colab]

# Setup and create enhanced pipeline
from prompt_refiner_anatomy.integration import create_educational_pipeline
import torch

pipe = create_educational_pipeline(
    device="cuda",
    torch_dtype=torch.float16  # Memory optimization for Colab
)

# Generate educational anatomical content with simple prompts
image = pipe("heart", focus="education")
image.images[0].show()

# Generate 3D-optimized content
skeleton = pipe("skeleton", focus="3d_modeling", view_type="cross_section")
skeleton.images[0].show()
```

## Example Transformations

| Input | Output Prompt |
|-------|---------------|
| `"heart"` | `"anatomical illustration of heart, medical textbook style, educational diagram, for grade school science class, educational poster style, orthographic projection, clean topology, neutral lighting"` |
| `"brain"` (cross-section) | `"anatomical illustration of brain, brain cross-section view, cutaway diagram, internal structure visible, educational diagram, orthographic view, clean topology, solid colors"` |

**Negative Prompt** (automatically generated): `"blood, gore, graphic, scary, disturbing, realistic skin texture, text, labels, annotations, arrows, numbers, watermarks"`

## Supported Body Systems

- **Skeletal System**: skull, spine, ribs, pelvis, femur, tibia, etc.
- **Circulatory System**: heart, arteries, veins, blood vessels
- **Respiratory System**: lungs, trachea, bronchi, diaphragm
- **Nervous System**: brain, spinal cord, nerves, neurons  
- **Digestive System**: stomach, intestines, liver, esophagus
- **Muscular System**: biceps, triceps, quadriceps, hamstrings

View all terms: `python -m prompt_refiner_anatomy --list-terms`

## Advanced Usage

### Python API

```python
from prompt_refiner_anatomy import PromptRefiner

refiner = PromptRefiner()

# Basic enhancement
result = refiner.enhance("heart")
print(f"Positive: {result['positive']}")
print(f"Negative: {result['negative']}")

# With specific focus and view type
result = refiner.enhance(
    "brain", 
    focus="3d_modeling",    # Options: education, 3d_modeling, scientific
    view_type="cross_section"  # Options: standard, cross_section, system_overview
)
```

### Batch Generation with Diffusers

```python
from prompt_refiner_anatomy.integration import DiffusersWrapper

# Wrap any existing pipeline
enhanced_pipe = DiffusersWrapper(your_pipeline)

# Generate multiple anatomical structures
organs = ["heart", "brain", "lungs", "liver", "kidneys"]
results = enhanced_pipe.generate_batch(
    organs, 
    focus="education",
    num_inference_steps=20
)
```

## Educational Focus

This tool is specifically designed for **Grade school educational content**:

- ✅ Age-appropriate anatomical terminology
- ✅ Simplified, clean illustrations  
- ✅ No graphic medical content
- ✅ Educational context built into every prompt
- ✅ Perfect for science class presentations

### Safety Features

- **Content Filtering**: Blocks blood, gore, surgical procedures, nudity
- **Term Replacement**: Converts advanced medical terms to K-6 appropriate language
- **Educational Context**: Always includes "educational", "science class", "diagram" context
- **Logging**: All content modifications are logged for transparency

## 3D Modeling Optimization

Generated images are optimized for 3D model creation:

- **Orthographic Views**: Better depth perception for modeling
- **Clean Topology**: "clean topology, solid colors" tags improve mesh generation  
- **Neutral Lighting**: Consistent lighting for accurate form reference
- **No Text/Labels**: Avoids annotations that confuse 3D software

## PowerShell Demo

Run the included PowerShell demo to generate a complete set of prompts:

```powershell
# Run the demo (Windows)
powershell.exe -ExecutionPolicy Bypass -File "examples\demo_ps.ps1"
```

This generates JSON files for multiple organs in both standard and 3D-optimized formats.

## Architecture

```
prompt_refiner_anatomy/
├── enhancer.py          # Core PromptRefiner class
├── filters.py           # Safety and educational filters  
├── data/
│   └── anatomical_terms.json  # Curated K-6 vocabulary
├── integration/
│   ├── diffusers_hook.py      # Google Colab integration
│   └── colab_utils.py         # Colab setup utilities
└── __main__.py          # CLI interface
```

## Contributing

We welcome contributions! The vocabulary database is designed to be easily extensible.

```python
# Add new organs to prompt_refiner_anatomy/data/anatomical_terms.json
{
  "body_systems": {
    "new_system": {
      "description": "K-6 appropriate description",
      "organs": ["organ1", "organ2"],
      "keywords": ["keyword1", "keyword2"]
    }
  }
}
```

## Requirements

- **Python 3.8+** (tested on 3.12)
- **No external dependencies** for core functionality
- **Optional**: `diffusers`, `torch`, `transformers` for Colab integration

## License

MIT License - see LICENSE file for details.

The anatomical vocabulary database is licensed under CC-BY-SA 4.0 for educational use.
