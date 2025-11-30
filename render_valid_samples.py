"""
Render PNG images from the 144 valid Claude-fixed code samples
Using PartToImage.py rendering approach
"""
import os
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from PartToImage import convert_part_to_image


# Configuration
VALIDATION_RESULTS = "data/claude_fixed_validation_results_simple.json"
CODE_DIR = "data/claude_fixed_code"
OUTPUT_DIR = "data/claude_fixed_renders"
MAX_WORKERS = 8

# Image settings
VIEW_TYPE = "iso"  # isometric view
RESOLUTION = 448
REMOVE_BG = True  # Remove white background


def render_single_file(code_path, output_path):
    """Render a single CadQuery Python file to PNG"""
    try:
        convert_part_to_image(
            file_name=code_path,
            view_type=VIEW_TYPE,
            save_path=output_path,
            b_rep_name="BRepName",
            remove_bg_flag=REMOVE_BG
        )

        # Check if output was created
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {
                'success': True,
                'file': os.path.basename(code_path),
                'output': output_path
            }
        else:
            return {
                'success': False,
                'file': os.path.basename(code_path),
                'error': 'No output file created'
            }

    except Exception as e:
        return {
            'success': False,
            'file': os.path.basename(code_path),
            'error': str(e)
        }


def main():
    print("=" * 60)
    print("Render Valid Claude-Fixed Samples to PNG")
    print("=" * 60)

    # Load validation results
    if not os.path.exists(VALIDATION_RESULTS):
        print(f"Error: {VALIDATION_RESULTS} not found!")
        print("Please run validate_claude_fixed_simple.py first.")
        return

    with open(VALIDATION_RESULTS, 'r') as f:
        validation_data = json.load(f)

    # Get list of valid files
    valid_files = [
        item['file'] for item in validation_data['files']
        if item['error_code'] == 0
    ]

    print(f"Found {len(valid_files)} valid files to render")
    print(f"View type: {VIEW_TYPE}")
    print(f"Resolution: {RESOLUTION}x{RESOLUTION}")
    print(f"Remove background: {REMOVE_BG}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Workers: {MAX_WORKERS}")
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Prepare tasks
    tasks = []
    for valid_file in valid_files:
        code_path = valid_file  # Already full path from validation
        base_name = os.path.basename(code_path).replace('.py', '')
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.png")
        tasks.append((code_path, output_path))

    # Process with progress bar
    results = {
        'total': len(tasks),
        'successful': 0,
        'failed': 0,
        'files': []
    }

    print(f"Processing {len(tasks)} files...\n")

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(render_single_file, code_path, output_path): (code_path, output_path)
            for code_path, output_path in tasks
        }

        with tqdm(total=len(tasks), desc="Rendering") as pbar:
            for future in as_completed(futures):
                result = future.result()

                if result['success']:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    error = result.get('error', 'Unknown')
                    tqdm.write(f"✗ {result['file']}: {error}")

                results['files'].append(result)
                pbar.update(1)

    # Summary
    print("\n" + "=" * 60)
    print("Rendering Summary")
    print("=" * 60)
    print(f"Total files:     {results['total']}")
    print(f"Successful:      {results['successful']}")
    print(f"Failed:          {results['failed']}")
    print("=" * 60)

    # Save results
    with open('render_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: render_results.json")
    print(f"PNG renders saved to: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
