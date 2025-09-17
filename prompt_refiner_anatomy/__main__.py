"""
Command-line interface for the Prompt Refiner Anatomy module.

Usage:
    python -m prompt_refiner_anatomy "heart"
    python -m prompt_refiner_anatomy "skeleton" --view-type cross_section
    python -m prompt_refiner_anatomy "brain" --focus 3d_modeling --output json
"""

import argparse
import json
import sys
from typing import Dict, Any

from . import PromptRefiner


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Enhance prompts for anatomical education content in Stable Diffusion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m prompt_refiner_anatomy "heart"
  python -m prompt_refiner_anatomy "skeleton" --view-type cross_section
  python -m prompt_refiner_anatomy "brain" --focus 3d_modeling --output json
  python -m prompt_refiner_anatomy --list-terms

Focus options:
  3d_reconstruction - Single organ on neutral background for 3D reconstruction
  education        - Clear educational medical diagrams
  scientific       - Detailed anatomical specimens for medical reference

View types:
  standard       - Basic anatomical illustration
  cross_section  - Cross-sectional/cutaway view
  system_overview - Overview of entire body system
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Anatomical term or phrase to enhance (e.g., 'heart', 'skeleton')"
    )
    
    parser.add_argument(
        "--focus",
        choices=["3d_reconstruction", "education", "scientific"],
        default=None,
        help="Focus area for optimization"
    )
    
    parser.add_argument(
        "--view-type",
        choices=["standard", "cross_section", "system_overview"],
        default="standard",
        help="Type of anatomical view to generate"
    )
    
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    
    parser.add_argument(
        "--list-terms",
        action="store_true",
        help="List all supported anatomical terms"
    )
    
    parser.add_argument(
        "--system-info",
        help="Get information about a specific body system"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Initialize the refiner
    try:
        refiner = PromptRefiner()
    except Exception as e:
        print(f"Error initializing PromptRefiner: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Handle special commands
    if args.list_terms:
        list_terms(refiner, args.output)
        return
    
    if args.system_info:
        show_system_info(refiner, args.system_info, args.output)
        return
    
    # Require prompt for enhancement
    if not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    # Enhance the prompt
    try:
        result = refiner.enhance(
            args.prompt,
            focus=args.focus,
            view_type=args.view_type
        )
        
        # Output results
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            print_text_output(result, args.verbose)
            
    except Exception as e:
        print(f"Error enhancing prompt: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def list_terms(refiner: PromptRefiner, output_format: str):
    """List all supported anatomical terms."""
    terms = refiner.list_supported_terms()
    
    if output_format == "json":
        print(json.dumps(terms, indent=2))
    else:
        print("Supported Anatomical Terms by Body System:")
        print("=" * 45)
        
        for system, system_terms in terms.items():
            print(f"\n{system.upper()}:")
            for term in sorted(system_terms):
                print(f"  • {term}")


def show_system_info(refiner: PromptRefiner, system_name: str, output_format: str):
    """Show information about a specific body system."""
    info = refiner.get_system_info(system_name.lower())
    
    if not info:
        print(f"Unknown body system: {system_name}", file=sys.stderr)
        print("Available systems:", ", ".join(refiner.list_supported_terms().keys()))
        sys.exit(1)
    
    if output_format == "json":
        print(json.dumps({system_name: info}, indent=2))
    else:
        print(f"Body System: {system_name.upper()}")
        print("=" * 30)
        print(f"Description: {info['description']}")
        print(f"\nOrgans: {', '.join(info['organs'])}")
        print(f"Keywords: {', '.join(info['keywords'])}")


def print_text_output(result: Dict[str, Any], verbose: bool = False):
    """Print enhancement results in human-readable format."""
    print("Enhanced Prompt Results")
    print("=" * 25)
    
    print(f"\nPositive Prompt:")
    print(f"  {result['positive']}")
    
    print(f"\nNegative Prompt:")
    print(f"  {result['negative']}")
    
    if verbose:
        if result.get('detected_terms'):
            print(f"\nDetected Terms: {', '.join(result['detected_terms'])}")
        
        if result.get('detected_systems'):
            print(f"Detected Systems: {', '.join(result['detected_systems'])}")
    
    print(f"\nReady for Stable Diffusion! 🎨")
    
    # Usage tip
    print(f"\n💡 Tip: Copy the positive and negative prompts above into your")
    print(f"   Stable Diffusion interface (Automatic1111, ComfyUI, etc.)")


if __name__ == "__main__":
    main()