"""
Complete pipeline: Gemini generation → Claude fixing → Validation → STEP export
Processes the remaining images (244-1000) from the dataset
"""
import os
import json
import sys
import subprocess
import tempfile
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import anthropic
import google.generativeai as genai
from PIL import Image

# Configuration
IMAGES_DIR = "data/sdg_abc_1k_images"
GEMINI_OUTPUT_DIR = "data/gemini_generated_code"
CLAUDE_OUTPUT_DIR = "data/claude_fixed_code"
VALIDATION_RESULTS_FILE = "data/pipeline_validation_results.json"

# API Configuration
GEMINI_MODEL = "gemini-2.0-flash-exp"
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
MAX_WORKERS = 8
TIMEOUT_SECONDS = 30

# Get API keys from environment
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not ANTHROPIC_API_KEY:
    print("Error: ANTHROPIC_API_KEY environment variable not set")
    sys.exit(1)
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set")
    sys.exit(1)

# Initialize clients
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(GEMINI_MODEL)

# Prompts
GEMINI_PROMPT = """Generate CadQuery Python code to create this 3D CAD model.

Requirements:
- Use CadQuery syntax
- Create a variable called 'result' containing the final geometry
- Include all necessary imports
- Use parametric dimensions where appropriate
- The code must be executable and create valid solid geometry

Return ONLY the Python code, no explanations."""

CLAUDE_FIXING_PROMPT = '''Fix the CadQuery API errors in this generated code.

COMMON ERRORS TO FIX:
1. `.filterBy(lambda ...)` - DOES NOT EXIST
   Fix: Remove filterBy() entirely

2. `.rect(center=(x,y), mode='a')` - parameters don't exist
   Fix: Use .center(x, y).rect(width, height) instead

3. `result.workplane("XY")` on existing workplane - causes error
   Fix: Use cq.Workplane("XY") for new workplane

4. `.translate((x, y, z))` - correct syntax
   NOT: `.move(x, y, z)` or `.position(x, y, z)`

5. Missing `import cadquery as cq` at the top

RULES:
- Keep the same design intent
- Fix API errors while preserving functionality
- Ensure 'result' variable contains final geometry
- Keep code structure similar to original
- ONLY return the fixed Python code, no explanations

Code to fix:
```python
{code}
```'''

ERROR_CODES = {
    0: "Success",
    1: "Ground truth reconstruction failed",
    2: "Generated code failed (syntax/runtime error)",
    3: "OCC computation failed",
    4: "Timeout",
    5: "Non-solid geometry",
    6: "Multiprocessing error"
}


def get_already_processed_files():
    """Get list of files that have already been successfully processed"""
    processed = set()

    # Check existing Gemini outputs
    if os.path.exists(GEMINI_OUTPUT_DIR):
        for f in os.listdir(GEMINI_OUTPUT_DIR):
            if f.endswith('.py'):
                processed.add(f.replace('.py', ''))

    # Check existing Claude outputs
    if os.path.exists(CLAUDE_OUTPUT_DIR):
        for f in os.listdir(CLAUDE_OUTPUT_DIR):
            if f.endswith('.py'):
                processed.add(f.replace('.py', ''))

    return processed


def generate_with_gemini(image_path):
    """Generate CadQuery code using Gemini"""
    try:
        image = Image.open(image_path)
        response = gemini_model.generate_content([GEMINI_PROMPT, image])

        if not response.text:
            return None, "Empty response from Gemini"

        # Extract code from markdown if present
        code = response.text
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()

        return code, None
    except Exception as e:
        return None, str(e)


def fix_with_claude(code):
    """Fix code using Claude"""
    try:
        message = anthropic_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": CLAUDE_FIXING_PROMPT.format(code=code)
            }]
        )

        fixed_code = message.content[0].text

        # Extract code from markdown if present
        if "```python" in fixed_code:
            fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
        elif "```" in fixed_code:
            fixed_code = fixed_code.split("```")[1].split("```")[0].strip()

        return fixed_code, None
    except Exception as e:
        return None, str(e)


def validate_code(code_path, timeout):
    """Validate CadQuery code by executing it"""
    try:
        with tempfile.NamedTemporaryFile(suffix='.step', delete=False) as tmp:
            step_file = tmp.name

        with open(code_path, 'r') as f:
            code = f.read()

        # Remove show_object() calls
        code = code.replace('show_object(result)', '')
        code = code.replace('show_object(', '# show_object(')

        template = f"""
import cadquery as cq

{code}

cq.exporters.export(result, '{step_file}')
"""

        # Write to temp Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_py:
            tmp_py_name = tmp_py.name
            tmp_py.write(template)

        # Execute with subprocess
        result = subprocess.run(
            [sys.executable, tmp_py_name],
            timeout=timeout,
            capture_output=True,
            text=True
        )

        # Clean up temp Python file
        os.unlink(tmp_py_name)

        if result.returncode != 0:
            error_msg = result.stderr if result.stderr else result.stdout
            if "SyntaxError" in error_msg:
                return 2, f"Syntax error: {error_msg[:200]}", None
            elif "NameError" in error_msg:
                return 2, f"Name error: {error_msg[:200]}", None
            elif "OCC" in error_msg or "opencascade" in error_msg.lower():
                return 3, f"OCC error: {error_msg[:200]}", None
            else:
                return 2, f"Runtime error: {error_msg[:200]}", None

        # Check if STEP file was created
        if os.path.exists(step_file) and os.path.getsize(step_file) > 0:
            return 0, None, step_file
        else:
            if os.path.exists(step_file):
                os.unlink(step_file)
            return 5, "No geometry created", None

    except subprocess.TimeoutExpired:
        if os.path.exists(tmp_py_name):
            os.unlink(tmp_py_name)
        return 4, f"Timeout after {timeout} seconds", None
    except Exception as e:
        return 6, f"Error: {str(e)}", None
    finally:
        if 'step_file' in locals() and os.path.exists(step_file):
            try:
                if 'step_file' not in str(locals().get('step_file', '')):
                    os.unlink(step_file)
            except:
                pass


def process_single_image(image_path, base_name):
    """Process a single image through the complete pipeline"""
    result = {
        'image': base_name,
        'gemini_success': False,
        'claude_success': False,
        'validation_code': None,
        'validation_error': None
    }

    # Step 1: Generate with Gemini
    gemini_code, gemini_error = generate_with_gemini(image_path)
    if gemini_error:
        result['gemini_error'] = gemini_error
        return result

    result['gemini_success'] = True

    # Save Gemini output
    gemini_output_path = os.path.join(GEMINI_OUTPUT_DIR, f"{base_name}.py")
    with open(gemini_output_path, 'w') as f:
        f.write(gemini_code)

    # Step 2: Fix with Claude
    claude_code, claude_error = fix_with_claude(gemini_code)
    if claude_error:
        result['claude_error'] = claude_error
        return result

    result['claude_success'] = True

    # Save Claude output
    claude_output_path = os.path.join(CLAUDE_OUTPUT_DIR, f"{base_name}.py")
    with open(claude_output_path, 'w') as f:
        f.write(claude_code)

    # Step 3: Validate code (check if it executes without error)
    error_code, error_msg, step_file = validate_code(claude_output_path, TIMEOUT_SECONDS)

    result['validation_code'] = error_code
    result['validation_error'] = error_msg

    # Clean up temporary STEP file
    if step_file and os.path.exists(step_file):
        os.unlink(step_file)

    return result


def main():
    print("=" * 60)
    print("Complete Pipeline: Gemini → Claude → Validation")
    print("=" * 60)

    # Start timing
    start_time = time.time()

    # Create output directories
    os.makedirs(GEMINI_OUTPUT_DIR, exist_ok=True)
    os.makedirs(CLAUDE_OUTPUT_DIR, exist_ok=True)

    # Get list of images
    images_path = Path(IMAGES_DIR)
    all_images = sorted(list(images_path.glob("*.png")))

    print(f"Found {len(all_images)} total images")

    # Filter out already processed
    already_processed = get_already_processed_files()
    images_to_process = [
        img for img in all_images
        if img.stem not in already_processed
    ]

    print(f"Already processed: {len(already_processed)}")
    print(f"Remaining to process: {len(images_to_process)}")
    print(f"Workers: {MAX_WORKERS}")
    print()

    if len(images_to_process) == 0:
        print("No images to process!")
        return

    # Process images
    results = {
        'total': len(images_to_process),
        'gemini_success': 0,
        'claude_success': 0,
        'validation_success': 0,
        'files': []
    }

    print(f"Processing {len(images_to_process)} images...\n")

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_single_image, str(img), img.stem): img
            for img in images_to_process
        }

        with tqdm(total=len(images_to_process), desc="Processing") as pbar:
            for future in as_completed(futures):
                result = future.result()

                if result['gemini_success']:
                    results['gemini_success'] += 1
                if result['claude_success']:
                    results['claude_success'] += 1
                if result['validation_code'] == 0:
                    results['validation_success'] += 1
                elif result.get('validation_error'):
                    error = result['validation_error']
                    tqdm.write(f"✗ {result['image']}: {error[:100]}")

                results['files'].append(result)
                pbar.update(1)

    # End timing
    end_time = time.time()
    total_time = end_time - start_time

    # Calculate costs
    # Gemini: Free tier (no cost calculation needed)
    # Claude Sonnet 4.5: $3/MTok input, $15/MTok output
    # Estimate: ~500 tokens input per request, ~1000 tokens output per request
    gemini_cost = 0  # Free tier
    claude_input_tokens = results['claude_success'] * 500
    claude_output_tokens = results['claude_success'] * 1000
    claude_cost = (claude_input_tokens / 1_000_000 * 3) + (claude_output_tokens / 1_000_000 * 15)
    total_cost = gemini_cost + claude_cost

    # Summary
    print("\n" + "=" * 60)
    print("Pipeline Summary")
    print("=" * 60)
    print(f"Total images:        {results['total']}")
    print(f"Gemini success:      {results['gemini_success']} ({100*results['gemini_success']/results['total']:.1f}%)")
    print(f"Claude success:      {results['claude_success']} ({100*results['claude_success']/results['total']:.1f}%)")
    print(f"Validation success:  {results['validation_success']} ({100*results['validation_success']/results['total']:.1f}%)")
    print()
    print(f"Total time:          {total_time/60:.1f} minutes ({total_time:.0f} seconds)")
    print(f"Time per image:      {total_time/results['total']:.1f} seconds")
    print()
    print(f"Estimated cost:")
    print(f"  Gemini:            $0.00 (free tier)")
    print(f"  Claude:            ${claude_cost:.2f}")
    print(f"  Total:             ${total_cost:.2f}")
    print("=" * 60)

    # Save results with timing and cost
    results['timing'] = {
        'total_seconds': total_time,
        'total_minutes': total_time / 60,
        'seconds_per_image': total_time / results['total']
    }
    results['costs'] = {
        'gemini_usd': gemini_cost,
        'claude_usd': claude_cost,
        'claude_input_tokens': claude_input_tokens,
        'claude_output_tokens': claude_output_tokens,
        'total_usd': total_cost
    }

    with open(VALIDATION_RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {VALIDATION_RESULTS_FILE}")
    print(f"\nPython files saved to:")
    print(f"  Gemini: {GEMINI_OUTPUT_DIR}/")
    print(f"  Claude: {CLAUDE_OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
