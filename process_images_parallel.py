"""
Process images with Gemini API in parallel to generate CadQuery code
"""
import os
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import google.generativeai as genai
from PIL import Image
from tqdm import tqdm

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_NAME = 'gemini-3-pro-preview'
INPUT_PRICE_PER_1M = 1.25
OUTPUT_PRICE_PER_1M = 5.00
IMAGE_DIR = "data/sdg_abc_1k_images"
OUTPUT_DIR = "data/cadquery_outputs"
CODE_OUTPUT_DIR = "data/generated_code"
MAX_WORKERS = 20  # Process 20 images in parallel

PROMPT = '''You are an expert CAD engineer. Analyze this 3D object image and generate CadQuery Python code to recreate it.

Requirements:
1. Study the geometry carefully: shapes, dimensions, holes, fillets, chamfers
2. Write complete, executable CadQuery code
3. Use the variable name 'result' for the final object
4. Code must be ready to execute as-is
5. Use proper CadQuery API methods

Generate only the Python code, nothing else.'''

def clean_code(code_text):
    """Extract Python code from markdown blocks"""
    if '```python' in code_text:
        code_text = code_text.split('```python')[1].split('```')[0]
    elif '```' in code_text:
        code_text = code_text.split('```')[1].split('```')[0]
    return code_text.strip()

def process_single_image(model, image_path, output_path, code_output_path):
    """Process a single image"""
    try:
        start_time = time.time()

        img = Image.open(image_path)
        response = model.generate_content([PROMPT, img])

        elapsed_time = time.time() - start_time

        code = response.text
        clean_code_text = clean_code(code)

        # Get metrics
        usage = response.usage_metadata
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        total_cost = (input_tokens / 1_000_000) * INPUT_PRICE_PER_1M + \
                     (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_1M

        # Prepare output
        output_data = {
            'image_path': str(image_path),
            'generated_code': code,
            'clean_code': clean_code_text,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost': total_cost,
            'time': elapsed_time,
            'model': MODEL_NAME
        }

        # Save JSON
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)

        # Save Python code
        os.makedirs(os.path.dirname(code_output_path), exist_ok=True)
        with open(code_output_path, 'w') as f:
            f.write(clean_code_text)

        return {
            'success': True,
            'file': os.path.basename(image_path),
            'cost': total_cost,
            'time': elapsed_time,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens
        }

    except Exception as e:
        return {
            'success': False,
            'file': os.path.basename(image_path),
            'error': str(e)
        }

def main():
    print("=" * 60)
    print("CadQuery Code Generation with Gemini (Parallel)")
    print("=" * 60)

    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable not set!")
        return

    # Setup
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CODE_OUTPUT_DIR, exist_ok=True)

    # Get all images
    image_files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith('.png')])
    print(f"Found {len(image_files)} images")
    print(f"Workers: {MAX_WORKERS} parallel")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Code: {CODE_OUTPUT_DIR}\n")

    # Prepare tasks
    tasks = []
    for image_file in image_files:
        image_path = os.path.join(IMAGE_DIR, image_file)
        output_path = os.path.join(OUTPUT_DIR, image_file.replace('.png', '.json'))
        code_output_path = os.path.join(CODE_OUTPUT_DIR, image_file.replace('.png', '.py'))

        # Skip if already processed
        if os.path.exists(output_path) and os.path.exists(code_output_path):
            continue

        tasks.append((model, image_path, output_path, code_output_path))

    if not tasks:
        print("All images already processed!")
        return

    print(f"Processing {len(tasks)} images...\n")

    # Initialize metrics
    metrics = {
        'total': len(tasks),
        'successful': 0,
        'failed': 0,
        'total_cost': 0,
        'total_time': 0,
        'total_input_tokens': 0,
        'total_output_tokens': 0
    }

    start_time = time.time()

    # Process in parallel with progress bar
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_image, *task): task for task in tasks}

        with tqdm(total=len(tasks), desc="Processing") as pbar:
            for future in as_completed(futures):
                result = future.result()

                if result['success']:
                    metrics['successful'] += 1
                    metrics['total_cost'] += result['cost']
                    metrics['total_time'] += result['time']
                    metrics['total_input_tokens'] += result['input_tokens']
                    metrics['total_output_tokens'] += result['output_tokens']

                    pbar.set_postfix({
                        'cost': f"${metrics['total_cost']:.2f}",
                        'avg': f"{metrics['total_cost']/metrics['successful']:.4f}"
                    })
                else:
                    metrics['failed'] += 1
                    tqdm.write(f"✗ Error: {result['file']} - {result.get('error', 'Unknown')}")

                pbar.update(1)

    elapsed = time.time() - start_time

    # Final summary
    print("\n" + "=" * 60)
    print("Processing Complete")
    print("=" * 60)
    print(f"Total images:    {metrics['total']}")
    print(f"Successful:      {metrics['successful']}")
    print(f"Failed:          {metrics['failed']}")
    print(f"\nTotal cost:      ${metrics['total_cost']:.2f}")
    print(f"Avg cost:        ${metrics['total_cost']/metrics['successful']:.4f} per image")
    print(f"\nTotal time:      {elapsed/3600:.2f} hours ({elapsed/60:.1f} minutes)")
    print(f"Throughput:      {metrics['successful']/(elapsed/60):.1f} images/minute")
    print(f"\nTokens:")
    print(f"  Input:         {metrics['total_input_tokens']:,}")
    print(f"  Output:        {metrics['total_output_tokens']:,}")
    print("=" * 60)

    # Save summary
    with open('generation_summary.json', 'w') as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    main()
