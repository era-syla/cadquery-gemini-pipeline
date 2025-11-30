"""
Export all 144 valid Claude-fixed code samples to STEP files
"""
import os
import json
import sys
import subprocess
import tempfile
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm


# Configuration
VALIDATION_RESULTS = "data/claude_fixed_validation_results_simple.json"
CODE_DIR = "data/claude_fixed_code"
OUTPUT_DIR = "data/claude_fixed_steps"
MAX_WORKERS = 8
TIMEOUT_SECONDS = 30


def export_single_file(code_path, step_path):
    """Export a single CadQuery Python file to STEP"""
    try:
        with open(code_path, 'r') as f:
            code = f.read()

        # Remove show_object() calls
        code = code.replace('show_object(result)', '')
        code = code.replace('show_object(', '# show_object(')

        # Create export script
        export_template = f"""
import cadquery as cq

{code}

cq.exporters.export(result, '{step_path}')
"""

        # Write and execute
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_py:
            tmp_py_name = tmp_py.name
            tmp_py.write(export_template)

        result = subprocess.run(
            [sys.executable, tmp_py_name],
            timeout=TIMEOUT_SECONDS,
            capture_output=True,
            text=True
        )

        os.unlink(tmp_py_name)

        if result.returncode == 0 and os.path.exists(step_path) and os.path.getsize(step_path) > 0:
            return {
                'success': True,
                'file': os.path.basename(code_path),
                'output': step_path,
                'size': os.path.getsize(step_path)
            }
        else:
            return {
                'success': False,
                'file': os.path.basename(code_path),
                'error': result.stderr[:200] if result.stderr else 'No STEP file created'
            }

    except subprocess.TimeoutExpired:
        if os.path.exists(tmp_py_name):
            os.unlink(tmp_py_name)
        return {
            'success': False,
            'file': os.path.basename(code_path),
            'error': f'Timeout after {TIMEOUT_SECONDS}s'
        }
    except Exception as e:
        return {
            'success': False,
            'file': os.path.basename(code_path),
            'error': str(e)
        }


def main():
    print("=" * 60)
    print("Export Valid Claude-Fixed Samples to STEP")
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

    print(f"Found {len(valid_files)} valid files to export")
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
        step_path = os.path.join(OUTPUT_DIR, f"{base_name}.step")
        tasks.append((code_path, step_path))

    # Process with progress bar
    results = {
        'total': len(tasks),
        'successful': 0,
        'failed': 0,
        'total_size': 0,
        'files': []
    }

    print(f"Processing {len(tasks)} files...\n")

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(export_single_file, code_path, step_path): (code_path, step_path)
            for code_path, step_path in tasks
        }

        with tqdm(total=len(tasks), desc="Exporting") as pbar:
            for future in as_completed(futures):
                result = future.result()

                if result['success']:
                    results['successful'] += 1
                    results['total_size'] += result.get('size', 0)
                else:
                    results['failed'] += 1
                    error = result.get('error', 'Unknown')
                    tqdm.write(f"✗ {result['file']}: {error}")

                results['files'].append(result)
                pbar.update(1)

    # Summary
    print("\n" + "=" * 60)
    print("Export Summary")
    print("=" * 60)
    print(f"Total files:     {results['total']}")
    print(f"Successful:      {results['successful']}")
    print(f"Failed:          {results['failed']}")
    print(f"Total size:      {results['total_size'] / 1024 / 1024:.2f} MB")
    print("=" * 60)

    # Save results
    with open('step_export_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: step_export_results.json")
    print(f"STEP files saved to: {OUTPUT_DIR}/")
    print(f"\nYou can now use these STEP files with PartToImage.py on a system with pythonOCC installed.")


if __name__ == "__main__":
    main()
