"""
Validate generated CadQuery code by executing it and exporting to STEP format
"""
import os
import sys
import tempfile
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, TimeoutError
import multiprocessing
import json
from datetime import datetime


GENERATED_CODE_DIR = "data/generated_code"
VALIDATION_RESULTS_FILE = "data/validation_results.json"
NUM_WORKERS = 64
TIMEOUT_SECONDS = 15

ERROR_CODES = {
    0: "Success",
    1: "Ground truth reconstruction failed",
    2: "Generated code failed (syntax/runtime error)",
    3: "OCC computation failed",
    4: "Timeout",
    5: "Non-solid geometry",
    6: "Multiprocessing error"
}


def validate_single_code(code_path):
    """
    Validate a single CadQuery Python file
    Returns: (code_path, status_code, error_message)
    """
    try:
        with tempfile.NamedTemporaryFile(suffix='.step', delete=False) as tmp:
            step_file = tmp.name

        with open(code_path, 'r') as f:
            code = f.read()

        template = f"""
import cadquery as cq

{code}

cq.exporters.export(result, '{step_file}')
"""

        namespace = {}
        exec(template, namespace)

        if os.path.exists(step_file) and os.path.getsize(step_file) > 0:
            os.unlink(step_file)
            return (str(code_path), 0, None)
        else:
            os.unlink(step_file) if os.path.exists(step_file) else None
            return (str(code_path), 5, "No geometry created")

    except SyntaxError as e:
        return (str(code_path), 2, f"Syntax error: {str(e)}")
    except NameError as e:
        return (str(code_path), 2, f"Name error: {str(e)}")
    except Exception as e:
        error_msg = str(e)
        if "OCC" in error_msg or "opencascade" in error_msg.lower():
            return (str(code_path), 3, f"OCC error: {error_msg}")
        else:
            return (str(code_path), 2, f"Runtime error: {error_msg}")
    finally:
        if 'step_file' in locals() and os.path.exists(step_file):
            try:
                os.unlink(step_file)
            except:
                pass


def validate_with_timeout(code_path, timeout):
    """Wrapper to validate with timeout"""
    try:
        with ProcessPoolExecutor(max_workers=1) as executor:
            future = executor.submit(validate_single_code, code_path)
            return future.result(timeout=timeout)
    except TimeoutError:
        return (str(code_path), 4, f"Timeout after {timeout} seconds")
    except Exception as e:
        return (str(code_path), 6, f"Multiprocessing error: {str(e)}")


def main():
    """Main validation process"""
    print("=" * 60)
    print("CadQuery Code Validation")
    print("=" * 60)

    code_dir = Path(GENERATED_CODE_DIR)
    if not code_dir.exists():
        print(f"Error: Directory {GENERATED_CODE_DIR} does not exist")
        return

    py_files = sorted(code_dir.glob("*.py"))
    total_files = len(py_files)

    print(f"\nFound {total_files} Python files to validate")
    print(f"Workers: {NUM_WORKERS}")
    print(f"Timeout: {TIMEOUT_SECONDS} seconds per file\n")

    results = {
        "total": total_files,
        "valid": 0,
        "invalid": 0,
        "errors_by_code": {code: 0 for code in ERROR_CODES.keys()},
        "files": {},
        "timestamp": datetime.now().isoformat()
    }

    print("Validating...")
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = {executor.submit(validate_with_timeout, py_file, TIMEOUT_SECONDS): py_file
                   for py_file in py_files}

        completed = 0
        for future in futures:
            file_path, status_code, error_msg = future.result()
            completed += 1

            file_name = Path(file_path).name
            results["files"][file_name] = {
                "status_code": status_code,
                "error": error_msg,
                "valid": status_code == 0
            }

            results["errors_by_code"][status_code] += 1
            if status_code == 0:
                results["valid"] += 1
                print(f"[{completed}/{total_files}] ✓ {file_name}")
            else:
                results["invalid"] += 1
                print(f"[{completed}/{total_files}] ✗ {file_name} - {ERROR_CODES.get(status_code, 'Unknown')}")

    # Save results
    with open(VALIDATION_RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)

    # Summary
    print("\n" + "=" * 60)
    print("Validation Complete")
    print("=" * 60)
    print(f"Total files:    {results['total']}")
    print(f"Valid:          {results['valid']} ({results['valid']/results['total']*100:.1f}%)")
    print(f"Invalid:        {results['invalid']} ({results['invalid']/results['total']*100:.1f}%)")
    print("\nError breakdown:")
    for code, count in sorted(results["errors_by_code"].items()):
        if count > 0:
            print(f"  {ERROR_CODES[code]}: {count}")
    print(f"\nResults saved to: {VALIDATION_RESULTS_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', force=True)
    main()
