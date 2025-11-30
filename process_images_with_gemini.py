"""
Process images with Gemini API to generate CadQuery code
"""
import os
import json
from pathlib import Path
import google.generativeai as genai
from PIL import Image
import time
from datetime import datetime
from dataclasses import dataclass, asdict

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Your API key
IMAGE_DIR = "data/sdg_abc_1k_images"
OUTPUT_DIR = "data/cadquery_outputs"
CODE_OUTPUT_DIR = "data/generated_code"  # Directory for Python files
METRICS_FILE = "data/processing_metrics.json"
MODEL_NAME = "gemini-3-pro-preview"  # Gemini 3 Pro Preview model

# Pricing (as of Nov 2024 - verify current pricing)
# Gemini 3 Pro pricing per million tokens
INPUT_PRICE_PER_1M = 1.25  # USD per 1M input tokens
OUTPUT_PRICE_PER_1M = 5.00  # USD per 1M output tokens

@dataclass
class ProcessingMetrics:
    """Track metrics for image processing"""
    total_images: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_usd: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0
    processing_times: list = None

    def __post_init__(self):
        if self.processing_times is None:
            self.processing_times = []

    @property
    def total_time_seconds(self):
        return self.end_time - self.start_time if self.end_time > 0 else 0

    @property
    def throughput_images_per_minute(self):
        if self.total_time_seconds > 0:
            return (self.successful / self.total_time_seconds) * 60
        return 0

    @property
    def avg_time_per_image(self):
        if self.processing_times:
            return sum(self.processing_times) / len(self.processing_times)
        return 0

# Prompt for Gemini
PROMPT = """You are an expert in CadQuery, a Python library for building parametric 3D CAD models.

Analyze this 3D rendered image and generate CadQuery code that would recreate this object.

CRITICAL: Generate code with ZERO comments. No # comments allowed anywhere in the code.

Requirements:
- Provide complete, executable CadQuery code
- Use proper CadQuery syntax and best practices
- The code should be self-contained and runnable
- Focus on accuracy of the visible geometry
- Store the final result in a variable named 'result'
- Use descriptive variable names instead of comments

Return ONLY the Python code with CadQuery commands, no additional explanation, no comments."""


def setup_gemini():
    """Initialize Gemini API"""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(MODEL_NAME)


def clean_code(code):
    """Remove markdown code fences if present"""
    code = code.strip()
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()


def process_image(model, image_path, output_path, code_output_path, metrics):
    """Process a single image with Gemini and track metrics"""
    start_time = time.time()

    try:
        # Load image
        img = Image.open(image_path)

        # Generate content
        response = model.generate_content([PROMPT, img])

        # Extract code from response
        code = response.text
        clean_code_text = clean_code(code)

        # Track token usage
        usage = response.usage_metadata
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count

        # Calculate cost
        input_cost = (input_tokens / 1_000_000) * INPUT_PRICE_PER_1M
        output_cost = (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_1M
        total_cost = input_cost + output_cost

        # Update metrics
        metrics.total_input_tokens += input_tokens
        metrics.total_output_tokens += output_tokens
        metrics.total_cost_usd += total_cost

        processing_time = time.time() - start_time
        metrics.processing_times.append(processing_time)

        # Save JSON output
        output_data = {
            "image_path": str(image_path),
            "generated_code": code,
            "timestamp": time.time(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": round(total_cost, 6),
            "processing_time_seconds": round(processing_time, 2)
        }

        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)

        # Save Python code file
        with open(code_output_path, 'w') as f:
            f.write(clean_code_text)

        print(f"✓ Processed: {image_path.name} "
              f"({input_tokens}+{output_tokens} tokens, "
              f"${total_cost:.4f}, {processing_time:.1f}s)")
        return True

    except Exception as e:
        print(f"✗ Error processing {image_path.name}: {str(e)}")
        return False


def save_metrics(metrics, filename):
    """Save metrics to JSON file"""
    metrics_dict = {
        "total_images": metrics.total_images,
        "successful": metrics.successful,
        "failed": metrics.failed,
        "skipped": metrics.skipped,
        "total_input_tokens": metrics.total_input_tokens,
        "total_output_tokens": metrics.total_output_tokens,
        "total_tokens": metrics.total_input_tokens + metrics.total_output_tokens,
        "total_cost_usd": round(metrics.total_cost_usd, 2),
        "total_time_seconds": round(metrics.total_time_seconds, 2),
        "total_time_minutes": round(metrics.total_time_seconds / 60, 2),
        "total_time_hours": round(metrics.total_time_seconds / 3600, 2),
        "throughput_images_per_minute": round(metrics.throughput_images_per_minute, 2),
        "avg_time_per_image_seconds": round(metrics.avg_time_per_image, 2),
        "avg_cost_per_image_usd": round(metrics.total_cost_usd / metrics.successful, 4) if metrics.successful > 0 else 0,
        "timestamp": datetime.now().isoformat(),
        "model": MODEL_NAME
    }

    with open(filename, 'w') as f:
        json.dump(metrics_dict, f, indent=2)


def main():
    """Main processing loop"""
    # Initialize metrics
    metrics = ProcessingMetrics()
    metrics.start_time = time.time()

    # Setup
    print("Setting up Gemini API...")
    model = setup_gemini()

    # Create output directories
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    code_output_dir = Path(CODE_OUTPUT_DIR)
    code_output_dir.mkdir(parents=True, exist_ok=True)

    # Get all images
    image_dir = Path(IMAGE_DIR)
    images = sorted(image_dir.glob("*.png"))
    metrics.total_images = len(images)

    print(f"\nFound {len(images)} images to process")
    print(f"Model: {MODEL_NAME}")
    print(f"JSON output: {OUTPUT_DIR}")
    print(f"Code output: {CODE_OUTPUT_DIR}\n")

    # Process each image
    for idx, image_path in enumerate(images, 1):
        # Create output filenames
        output_filename = image_path.stem + ".json"
        output_path = output_dir / output_filename

        code_filename = image_path.stem + ".py"
        code_output_path = code_output_dir / code_filename

        # Skip if already processed
        if output_path.exists():
            print(f"⊘ Skipped (already exists): {image_path.name}")
            metrics.skipped += 1
            continue

        # Process image
        print(f"[{idx}/{len(images)}] Processing {image_path.name}...")

        if process_image(model, image_path, output_path, code_output_path, metrics):
            metrics.successful += 1
        else:
            metrics.failed += 1

        # Rate limiting - be nice to the API
        time.sleep(1)  # Adjust as needed

        # Save metrics after each image (in case of interruption)
        metrics.end_time = time.time()
        save_metrics(metrics, METRICS_FILE)

    # Final metrics
    metrics.end_time = time.time()
    save_metrics(metrics, METRICS_FILE)

    # Summary
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"{'='*60}")
    print(f"Images:")
    print(f"  Total:      {metrics.total_images}")
    print(f"  Successful: {metrics.successful}")
    print(f"  Failed:     {metrics.failed}")
    print(f"  Skipped:    {metrics.skipped}")
    print(f"\nTokens:")
    print(f"  Input:      {metrics.total_input_tokens:,}")
    print(f"  Output:     {metrics.total_output_tokens:,}")
    print(f"  Total:      {metrics.total_input_tokens + metrics.total_output_tokens:,}")
    print(f"\nCost:")
    print(f"  Total:      ${metrics.total_cost_usd:.2f}")
    print(f"  Per image:  ${metrics.total_cost_usd / metrics.successful:.4f}" if metrics.successful > 0 else "  Per image:  N/A")
    print(f"\nTime:")
    print(f"  Total:      {metrics.total_time_seconds / 60:.1f} minutes ({metrics.total_time_seconds / 3600:.2f} hours)")
    print(f"  Per image:  {metrics.avg_time_per_image:.2f} seconds")
    print(f"\nThroughput:")
    print(f"  {metrics.throughput_images_per_minute:.2f} images/minute")
    print(f"\nMetrics saved to: {METRICS_FILE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
