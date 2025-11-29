"""
Generate images from validated CadQuery code
Renders 3D geometry to PNG images at 448x448 resolution
"""
import os
from pathlib import Path
import json
from tqdm import tqdm
from PartToImage import convert_part_to_image


GENERATED_CODE_DIR = "data/generated_code"
OUTPUT_IMAGE_DIR = "data/generated_code_images"
VALIDATION_RESULTS_FILE = "data/validation_results.json"
IMAGE_SIZE = 448


def load_validation_results():
    """Load validation results to only process valid files"""
    if not os.path.exists(VALIDATION_RESULTS_FILE):
        print(f"Warning: {VALIDATION_RESULTS_FILE} not found")
        print("All files will be processed")
        return None

    with open(VALIDATION_RESULTS_FILE, 'r') as f:
        return json.load(f)


def get_cad_paths(root_dir):
    """Get all CAD file paths"""
    model_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.step', '.obj', '.py')):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)
                model_paths.append(rel_path)
    return model_paths


def main():
    """Main image generation process"""
    print("=" * 60)
    print("CadQuery Image Generation")
    print("=" * 60)

    # Create output directory
    os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_IMAGE_DIR}")

    # Load validation results
    validation_data = load_validation_results()

    # Get all CAD files
    print(f"Input directory: {GENERATED_CODE_DIR}")
    all_cad_files = get_cad_paths(GENERATED_CODE_DIR)

    if not all_cad_files:
        print(f"Error: No CAD files found in {GENERATED_CODE_DIR}")
        return

    print(f"Found {len(all_cad_files)} CAD files")
    print(f"Image size: {IMAGE_SIZE}x{IMAGE_SIZE}")
    print(f"View: Isometric\n")

    successful = 0
    failed = 0
    skipped = 0

    for file in tqdm(all_cad_files, desc="Rendering"):
        file_name = Path(file).name

        # Check validation if available
        if validation_data:
            file_info = validation_data.get("files", {}).get(file_name)
            if not file_info or not file_info.get("valid"):
                skipped += 1
                continue

        # Prepare paths
        input_path = os.path.join(GENERATED_CODE_DIR, file)
        png_name = os.path.splitext(file)[0] + ".png"
        png_name = png_name.replace("/", "_")
        output_path = os.path.join(OUTPUT_IMAGE_DIR, png_name)

        # Skip if already exists
        if os.path.exists(output_path):
            skipped += 1
            continue

        # Render image
        try:
            convert_part_to_image(
                input_path,
                "iso",
                output_path,
                "BRepName",
                resolution_height=IMAGE_SIZE,
                resolution_width=IMAGE_SIZE,
                remove_bg_flag=True
            )
            successful += 1
        except Exception as e:
            print(f"\n✗ Error rendering {file_name}: {str(e)}")
            failed += 1
            continue

    # Summary
    print("\n" + "=" * 60)
    print("Rendering Complete")
    print("=" * 60)
    print(f"Total files:    {len(all_cad_files)}")
    print(f"Successful:     {successful}")
    print(f"Failed:         {failed}")
    print(f"Skipped:        {skipped}")
    print("=" * 60)


if __name__ == "__main__":
    main()
