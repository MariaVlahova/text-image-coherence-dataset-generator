"""
Main script to generate COMPLEX presentation style images only.
This file generates images with ALL features enabled:
- Tables (always enabled, larger sizes)
- Logos (always enabled)
- Multiple inline images (always 2 images)
- Multiple text lines (title + text1 + text2)
- Bullets (always enabled)
- Borders (always enabled)
"""

import random
import os
import json
from datetime import datetime
from llm_text_generator import LLMTextGenerator
from slide_generator import generate_image, setup_dummy_assets, create_complex_images
import pandas as pd


# ============================================================
# CONFIGURATION - Complex Images Only
# ============================================================

# Dataset settings
NUM_SAMPLES = 1  # Number of image pairs to generate
OUTPUT_DIR = "generated_data"  # Subfolder where dataset will be saved

# LLM settings for text generation
USE_LLM = True  # Set to True to use LLM for text generation, False to use hardcoded lists
LLM_PROVIDER = "openai"  # Options: "openai", "ollama", "deepseek"
#   - "ollama": FREE, local, no API key needed. Install from https://ollama.com
#   - "openai": ~$0.15/million tokens. Get API key from https://platform.openai.com/api-keys
#   - "deepseek": Cost-effective alternative. Get API key from https://platform.deepseek.com
LLM_API_KEY = "your-key"  # Set to your API key, or None to read from environment variable
#   For OpenAI: Set environment variable: $env:OPENAI_API_KEY = "your-key" (PowerShell)
#   For DeepSeek: Set environment variable: $env:DEEPSEEK_API_KEY = "your-key" (PowerShell)
#   For Ollama: Leave as None (no API key needed)
GENERATE_PRESENTATION_TEXT = True  # Generate presentation text by analyzing the image (requires USE_LLM=True and vision-capable model)
PRESENTATION_TEXT_MAX_LENGTH = 400  # Maximum length of presentation text in characters

# Table settings - LARGER tables for complexity
TABLE_MIN_ROWS = 2
TABLE_MAX_ROWS = 4
TABLE_MIN_COLS = 2
TABLE_MAX_COLS = 4

# Image size settings - LARGER images
img_size = (224, 224)  # Width x Height in pixels (larger than default)
logo_size = (20, 20)  # Scaled for 224x224

# Font settings (more fonts for variety)
font_list = [
    "C:\\Windows\\Fonts\\arial.ttf",
    "C:\\Windows\\Fonts\\arialbd.ttf",
    "C:\\Windows\\Fonts\\times.ttf",
    "C:\\Windows\\Fonts\\timesbd.ttf",
    "C:\\Windows\\Fonts\\verdana.ttf",
    "C:\\Windows\\Fonts\\verdanab.ttf",
    "C:\\Windows\\Fonts\\calibri.ttf",
    "C:\\Windows\\Fonts\\calibrib.ttf",
    "C:\\Windows\\Fonts\\georgia.ttf",
    "C:\\Windows\\Fonts\\georgiab.ttf"
]

# Color settings - more variety
background_colors = [
    "#FFFFFF", "#FAFAFA", "#F5F5F5", "#F0F0F0", "#E8E8E8", 
    "#E0E0E0", "#D3D3D3", "#FFF8DC", "#F5F5DC", "#FDF5E6"
]
text_colors = [
    "#000000", "#0A0A0A", "#141414", "#1a1a1a", "#1F1F1F",
    "#262626", "#2c2c2c", "#333333", "#3D3D3D", "#404040"
]
border_color = "#000000"

# Border settings - thicker borders
border = [2, 3, 4, 5]

# Logo settings
logo_path = ["data/OIP.png", "data/OIP (1).png", "data/OIP (2).png", "data/OIP (3).png", "data/OIP (4).png", "data/OIP (5).png"]
logo_position = ["top-left", "top-right", "bottom-left", "bottom-right"]

# Inline image settings - always use 2 images
inline_img = ["data/pres2.png", "data/pres3.png", "data/pres4.png", "data/pres5.png", "data/pres6.png"]

# Table settings - thicker borders
table_borders = [2, 3, 4]
table_border_colors = [
    "#000000", "#1a1a1a", "#262626", "#333333", "#404040",
    "#4d4d4d", "#555555", "#595959", "#666666"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

# Initialize LLM text generator (global instance)
llm_generator = LLMTextGenerator(
    provider=LLM_PROVIDER,
    api_key=LLM_API_KEY,
    enabled=USE_LLM
)


def save_dataset_info(output_dir, images, presentation_texts, config):
    """Save dataset metadata to a JSON file with presentation texts."""
    metadata = {
        "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "num_samples": len(images),
        "complex_images": True,
        "all_features_enabled": True,
        "presentation_texts_enabled": GENERATE_PRESENTATION_TEXT,
        "configuration": config,
        "dataset": []
    }
    
    for idx, (img_path, presentation_text) in enumerate(zip(images, presentation_texts)):
        metadata["dataset"].append({
            "image_id": idx,
            "image_path": img_path,
            "presentation_text": presentation_text,
            "filename": os.path.basename(img_path)
        })
    
    metadata_path = os.path.join(output_dir, "dataset_metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\nDataset metadata saved to: {metadata_path}")
    
    # Also save presentation texts in a separate text file for easy reading
    if GENERATE_PRESENTATION_TEXT and presentation_texts:
        texts_path = os.path.join(output_dir, "presentation_texts.txt")
        with open(texts_path, 'w', encoding='utf-8') as f:
            for idx, (img_path, text) in enumerate(zip(images, presentation_texts)):
                f.write(f"=== Slide {idx}: {os.path.basename(img_path)} ===\n")
                f.write(f"{text}\n\n")
        print(f"Presentation texts saved to: {texts_path}")


# ============================================================
# MAIN EXECUTION
# ============================================================
# create_complex_images has been moved to slide_generator.py

def main():
    """Main function to generate complex images dataset."""
    print("=" * 70)
    print("COMPLEX PRESENTATION STYLE DATASET GENERATOR")
    print("All features enabled: Tables, Logos, 2 Images, Bullets, Borders")
    print("=" * 70)
    print()
    
    # Print LLM configuration status
    if USE_LLM:
        print(f"LLM Text Generation: ENABLED ({LLM_PROVIDER})")
        if LLM_PROVIDER == "openai":
            api_key_status = "✓ Set" if (LLM_API_KEY or os.getenv("OPENAI_API_KEY")) else "✗ Not set (will use fallback)"
            print(f"  API Key: {api_key_status}")
            if not (LLM_API_KEY or os.getenv("OPENAI_API_KEY")):
                print("  → Set OPENAI_API_KEY environment variable or set LLM_API_KEY in config")
        elif LLM_PROVIDER == "deepseek":
            api_key_status = "✓ Set" if (LLM_API_KEY or os.getenv("DEEPSEEK_API_KEY")) else "✗ Not set (will use fallback)"
            print(f"  API Key: {api_key_status}")
            if not (LLM_API_KEY or os.getenv("DEEPSEEK_API_KEY")):
                print("  → Set DEEPSEEK_API_KEY environment variable or set LLM_API_KEY in config")
        elif LLM_PROVIDER == "ollama":
            print("  → Using local Ollama instance (default: http://localhost:11434)")
        if GENERATE_PRESENTATION_TEXT:
            print(f"  Presentation Text Generation: ENABLED (Vision Model)")
            print(f"    → Analyzing images to generate text (max length: {PRESENTATION_TEXT_MAX_LENGTH} chars)")
        else:
            print(f"  Presentation Text Generation: DISABLED")
        print()
    else:
        print("LLM Text Generation: DISABLED (using hardcoded text lists)")
        if GENERATE_PRESENTATION_TEXT:
            print("  Note: GENERATE_PRESENTATION_TEXT requires USE_LLM=True")
        print()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print()
    
    setup_dummy_assets(logo_path, logo_size, inline_img)
    
    config = {
        "num_samples": NUM_SAMPLES,
        "table_min_rows": TABLE_MIN_ROWS,
        "table_max_rows": TABLE_MAX_ROWS,
        "table_min_cols": TABLE_MIN_COLS,
        "table_max_cols": TABLE_MAX_COLS,
        "image_size": img_size,
        "fonts": font_list,
        "background_colors": background_colors,
        "text_colors": text_colors,
        "complex_mode": True,
        "features": {
            "tables": "always_enabled",
            "logos": "always_enabled",
            "inline_images": "always_2_images",
            "bullets": "always_enabled",
            "borders": "always_enabled"
        }
    }
    
    print("Configuration:")
    print(f"  - Number of samples: {NUM_SAMPLES}")
    print(f"  - Table rows: {TABLE_MIN_ROWS}-{TABLE_MAX_ROWS}")
    print(f"  - Table columns: {TABLE_MIN_COLS}-{TABLE_MAX_COLS}")
    print(f"  - Image size: {img_size[0]}x{img_size[1]}")
    print(f"  - Complex mode: ALL features enabled")
    print()
    
    print("Generating complex dataset...")
    print("-" * 70)
    
    # Prepare configuration dictionary for create_complex_images
    config = {
        'img_size': img_size,
        'logo_size': logo_size,
        'font_list': font_list,
        'background_colors': background_colors,
        'text_colors': text_colors,
        'border_color': border_color,
        'border': border,
        'logo_path': logo_path,
        'logo_position': logo_position,
        'inline_img': inline_img,
        'table_borders': table_borders,
        'table_border_colors': table_border_colors,
        'table_min_rows': TABLE_MIN_ROWS,
        'table_max_rows': TABLE_MAX_ROWS,
        'table_min_cols': TABLE_MIN_COLS,
        'table_max_cols': TABLE_MAX_COLS,
        'generate_presentation_text': GENERATE_PRESENTATION_TEXT,
        'use_llm': USE_LLM,
        'presentation_text_max_length': PRESENTATION_TEXT_MAX_LENGTH
    }
    
    images, presentation_texts, full_data = create_complex_images(
        dataset_directory=OUTPUT_DIR,
        num_samples=NUM_SAMPLES,
        llm_generator=llm_generator,
        config=config
    )
    
    # Save dataset metadata with presentation texts
    save_dataset_info(OUTPUT_DIR, images, presentation_texts, config)
    df_result = pd.DataFrame(full_data)
    df_result.to_csv("result.csv", index=False)

    print("=" * 70)
    print("COMPLEX DATASET GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\nCheck the '{OUTPUT_DIR}' folder for your generated images.")
    print(f"Total files created: {NUM_SAMPLES} images")
    if GENERATE_PRESENTATION_TEXT:
        print(f"Presentation texts generated: {len(presentation_texts)} texts")
    print()


if __name__ == "__main__":
    main()

