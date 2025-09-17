# Prompt Refiner Anatomy - PowerShell Demo
# Educational anatomical content generation for Stable Diffusion

Write-Host "Prompt Refiner Anatomy - PowerShell Demo" -ForegroundColor Cyan
Write-Host "=" * 50

# Check if the module is available
try {
    python -m prompt_refiner_anatomy --help | Out-Null
    Write-Host "[OK] Prompt Refiner Anatomy module found" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Module not found. Please install with: pip install prompt-refiner-anatomy" -ForegroundColor Red
    exit 1
}

# Define anatomical terms to generate
$organs = @("heart", "brain", "lungs", "skeleton", "liver")
$output_dir = ".\generated_prompts"

# Create output directory
if (!(Test-Path $output_dir)) {
    New-Item -ItemType Directory -Path $output_dir | Out-Null
    Write-Host "[INFO] Created output directory: $output_dir" -ForegroundColor Yellow
}

Write-Host "`nGenerating enhanced prompts for anatomical terms..." -ForegroundColor Cyan

foreach ($organ in $organs) {
    Write-Host "`nProcessing: $organ" -ForegroundColor White
    
    # Generate standard view
    $standard_output = python -m prompt_refiner_anatomy $organ --output json
    $standard_file = "$output_dir\${organ}_standard.json"
    $standard_output | Out-File -FilePath $standard_file -Encoding UTF8
    
    # Generate cross-section view for 3D modeling
    $cross_section_output = python -m prompt_refiner_anatomy $organ --view-type cross_section --focus 3d_modeling --output json
    $cross_section_file = "$output_dir\${organ}_3d.json"
    $cross_section_output | Out-File -FilePath $cross_section_file -Encoding UTF8
    
    Write-Host "  [OK] Standard view: $standard_file" -ForegroundColor Green
    Write-Host "  [OK] 3D optimized: $cross_section_file" -ForegroundColor Green
}

# Display a sample result
Write-Host "`nSample Enhanced Prompt:" -ForegroundColor Cyan
Write-Host "-" * 30
python -m prompt_refiner_anatomy "heart" --verbose

Write-Host "`nTips for Google Colab Usage:" -ForegroundColor Yellow
Write-Host "1. Upload this module to Colab: !pip install prompt-refiner-anatomy[colab]" -ForegroundColor White
Write-Host "2. Use the integration: from prompt_refiner_anatomy.integration import create_educational_pipeline" -ForegroundColor White
Write-Host "3. Generate images: pipe = create_educational_pipeline(); pipe('heart')" -ForegroundColor White

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "- Copy prompts from $output_dir to your Stable Diffusion interface" -ForegroundColor White
Write-Host "- Use positive and negative prompts for best results" -ForegroundColor White
Write-Host "- For 3D modeling, use the *_3d.json files" -ForegroundColor White

Write-Host "`nDemo completed successfully!" -ForegroundColor Green
