"""
Main script to generate the presentation style dataset.
Run this file to create a balanced dataset of image pairs.
"""

import random
import os
from PIL import Image, ImageDraw, ImageFont
from datasetGenaratorPStyle import create_balanced_dataset, generate_table_data
import json
from datetime import datetime


# ============================================================
# CONFIGURATION - Adjust these settings as needed
# ============================================================

# Dataset settings
NUM_SAMPLES = 50  # Number of image pairs to generate
OUTPUT_DIR = "data"  # Subfolder where dataset will be saved

# Table settings
TABLE_MIN_ROWS = 2
TABLE_MAX_ROWS = 5
TABLE_MIN_COLS = 2
TABLE_MAX_COLS = 4

# Image size settings
img_size = (224, 224)  # Width x Height in pixels
logo_size = (40, 40)

# Font settings (adjust paths for your system)
# For Windows, common fonts are in C:\Windows\Fonts\
font_list = [
    "C:\\Windows\\Fonts\\arial.ttf",
    "C:\\Windows\\Fonts\\times.ttf",
    "C:\\Windows\\Fonts\\verdana.ttf",
    "C:\\Windows\\Fonts\\calibri.ttf"
]

# Alternative: use font names (may not work on all systems)
# font_list = ["arial.ttf", "times.ttf", "verdana.ttf", "calibri.ttf"]

# Color settings
background_colors = ["#FFFFFF", "#F5F5F5", "#E8E8E8", "#FAFAFA"]
text_colors = ["#000000", "#1a1a1a", "#333333", "#2c2c2c"]
border_color = "#000000"

# Border settings
border = [1, 2, 3, 4]

# Logo settings (create dummy logos or use your own)
logo_path = ["logo1.png", "logo2.png", "logo3.png"]
logo_position = ["top-left", "top-right", "bottom-left", "bottom-right"]

# Inline image settings (create dummy images or use your own)
inline_img = ["inline1.png", "inline2.png", "inline3.png"]

# Table settings
table_borders = [1, 2, 3, 4]
table_border_colors = ["#000000", "#333333", "#555555", "#777777"]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_random_text():
    """Generates random text for presentations."""
    text_samples = [
        "Market Analysis Q4 2024",
        "Revenue Growth Strategy",
        "Customer Engagement Metrics",
        "Product Development Roadmap",
        "Team Performance Overview",
        "Annual Budget Forecast",
        "Digital Transformation Initiative",
        "Competitive Market Position",
        "Innovation and Research",
        "Sustainability Goals 2025",
        "Key Performance Indicators",
        "Strategic Partnership Opportunities",
        "Sales Pipeline Analysis",
        "Brand Awareness Campaign",
        "Operational Efficiency Metrics",
        "Technology Stack Overview",
        "Employee Retention Programs",
        "Customer Satisfaction Survey",
        "Market Expansion Plans",
        "Risk Management Framework"
    ]
    return random.choice(text_samples)


def wrap_text_by_words(text, draw, font, max_width):
    """
    Wraps text into multiple lines without splitting words.
    
    Args:
        text: The text to wrap
        draw: PIL ImageDraw object for measuring text
        font: PIL ImageFont object
        max_width: Maximum width in pixels for each line
    
    Returns:
        List of text lines
    """
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        # Test if adding this word would exceed the width
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            # Current line is full, start a new line
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    # Add the last line if it has content
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines if lines else [text]


def create_dummy_image(path, size=(200, 150), color="#4A90E2", label="IMAGE"):
    """Creates a dummy placeholder image."""
    if not os.path.exists(path):
        img = Image.new('RGB', size, color=color)
        draw = ImageDraw.Draw(img)
        
        # Draw border
        draw.rectangle([0, 0, size[0]-1, size[1]-1], outline="#FFFFFF", width=3)
        
        # Draw text in center
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Get text size for centering
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (size[0] - text_width) // 2
        text_y = (size[1] - text_height) // 2
        
        draw.text((text_x, text_y), label, fill="#FFFFFF", font=font)
        img.save(path)
        print(f"Created dummy image: {path}")


def generate_image(font_path, img_background_color, output_path, text_color, 
                   img_size, font_size, title_font_size, line_spacing, 
                   logo_size, border, border_color, border_width, logo_path, 
                   logo_position, add_image, add_image_2, title, text1, text2, 
                   bullet, add_table, table_headers, table_data, 
                   table_border, table_border_color):
    """
    Generates a presentation slide image with all specified attributes.
    """
    # Create a new image
    img = Image.new('RGB', img_size, color=img_background_color)
    draw = ImageDraw.Draw(img)
    
    # Add border if enabled
    if border:
        for i in range(border_width):
            draw.rectangle([i, i, img_size[0]-1-i, img_size[1]-1-i], 
                         outline=border_color, width=1)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype(font_path, title_font_size)
        text_font = ImageFont.truetype(font_path, font_size)
        small_font = ImageFont.truetype(font_path, max(12, font_size - 4))
    except Exception as e:
        print(f"Warning: Could not load font {font_path}, using default. Error: {e}")
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Calculate initial y_position, accounting for top-positioned logos
    base_y_position = 60 + border_width * 5
    x_margin = 80 + border_width * 5
    
    # Check if logo is in top position and adjust title position accordingly
    if logo_path and logo_position in ["top-left", "top-right"] and os.path.exists(logo_path):
        # Logo is at y=20, with height logo_size[1], so title should start below it
        logo_bottom = 20 + logo_size[1]
        y_position = max(base_y_position, logo_bottom + 10)  # Add 10px padding below logo
    else:
        y_position = base_y_position
    
    # Draw title with word wrapping
    if title:
        # Calculate available width for title (account for logo if present)
        if logo_path and logo_position in ["top-right"] and os.path.exists(logo_path):
            # Logo is on the right, reduce available width
            max_title_width = img_size[0] - x_margin - logo_size[0] - 40  # 40px spacing from logo
        elif logo_path and logo_position in ["top-left"] and os.path.exists(logo_path):
            # Logo is on the left, but title starts after x_margin which should be after logo
            # So we still use full width minus margins
            max_title_width = img_size[0] - 2 * x_margin
        else:
            max_title_width = img_size[0] - 2 * x_margin
        
        # Wrap title into multiple lines
        title_lines = wrap_text_by_words(title, draw, title_font, max_title_width)
        
        # Draw each line of the title
        for line in title_lines:
            draw.text((x_margin, y_position), line, fill=text_color, font=title_font)
            y_position += title_font_size + line_spacing * 5  # Smaller spacing between title lines
        
        y_position += line_spacing * 5  # Extra spacing after last title line
        
        # Draw a line separating title from text
        line_y = y_position + 10
        line_start_x = x_margin
        line_end_x = img_size[0] - x_margin
        draw.line([(line_start_x, line_y), (line_end_x, line_y)], 
                 fill=text_color, width=2)
        y_position = line_y + 20
    
    # Draw text1
    if text1:
        prefix = "• " if bullet else ""
        draw.text((x_margin + (20 if bullet else 0), y_position), 
                 f"{prefix}{text1}", fill=text_color, font=text_font)
        y_position += font_size + line_spacing * 12
    
    # Draw text2
    if text2:
        prefix = "• " if bullet else ""
        draw.text((x_margin + (20 if bullet else 0), y_position), 
                 f"{prefix}{text2}", fill=text_color, font=text_font)
        y_position += font_size + line_spacing * 12
    
    y_position += 30
    
    # Draw table
    if add_table and table_headers and table_data:
        table_x = x_margin
        table_y = y_position
        table_width = min(700, img_size[0] - 2 * x_margin)
        
        num_cols = len(table_headers)
        num_rows = len(table_data)
        cell_width = table_width // num_cols
        cell_height = 40
        
        # Draw table border
        table_height = (num_rows + 1) * cell_height
        draw.rectangle([table_x, table_y, table_x + table_width, table_y + table_height],
                      outline=table_border_color, width=table_border)
        
        # Draw headers
        for col_idx, header in enumerate(table_headers):
            cell_x = table_x + col_idx * cell_width
            # Draw cell border
            draw.rectangle([cell_x, table_y, cell_x + cell_width, table_y + cell_height],
                         outline=table_border_color, width=max(1, table_border - 1))
            # Draw text
            draw.text((cell_x + 10, table_y + 12), str(header), 
                     fill=text_color, font=small_font)
        
        # Draw data rows
        for row_idx, row_data in enumerate(table_data):
            row_y = table_y + (row_idx + 1) * cell_height
            for col_idx, cell_data in enumerate(row_data):
                cell_x = table_x + col_idx * cell_width
                # Draw cell border
                draw.rectangle([cell_x, row_y, cell_x + cell_width, row_y + cell_height],
                             outline=table_border_color, width=max(1, table_border - 1))
                # Draw text
                draw.text((cell_x + 10, row_y + 12), str(cell_data), 
                         fill=text_color, font=small_font)
        
        y_position += table_height + 40
    
    # Draw inline images
    # Minimum image size
    min_img_size = 224
    
    # Calculate available space for images
    available_height = img_size[1] - y_position - 20  # Leave 20px margin at bottom
    
    # Check if there's a bottom logo that would reduce available height
    if logo_path and logo_position in ["bottom-left", "bottom-right"] and os.path.exists(logo_path):
        available_height = img_size[1] - y_position - logo_size[1] - 30  # Leave space for logo + padding
    
    # Ensure available_height is positive
    available_height = max(available_height, min_img_size) if available_height > 0 else min_img_size
    
    # Calculate available width
    available_width = img_size[0] - 2 * x_margin
    # Maximum image size (use available space but keep some margin)
    max_img_size = min(available_width, available_height, 400)  # Cap at 400px for reasonable size
    
    # Use larger size if available space allows, but at least the minimum
    inline_img_size = (max(min_img_size, max_img_size), max(min_img_size, max_img_size))
    
    if add_image and add_image_2:
        # Two images side by side
        img_spacing = 30
        # Calculate size for two images side by side
        total_available_width = available_width - img_spacing
        single_img_width = total_available_width // 2
        single_img_height = min(available_height, single_img_width)  # Keep square aspect
        
        inline_img_size = (single_img_width, single_img_height)
        
        img1_x = x_margin
        img2_x = x_margin + inline_img_size[0] + img_spacing
        
        if os.path.exists(add_image):
            try:
                inline1 = Image.open(add_image).resize(inline_img_size)
                img.paste(inline1, (img1_x, y_position))
            except:
                draw.rectangle([img1_x, y_position, 
                              img1_x + inline_img_size[0], 
                              y_position + inline_img_size[1]], 
                             outline=text_color, width=2)
        
        if os.path.exists(add_image_2):
            try:
                inline2 = Image.open(add_image_2).resize(inline_img_size)
                img.paste(inline2, (img2_x, y_position))
            except:
                draw.rectangle([img2_x, y_position, 
                              img2_x + inline_img_size[0], 
                              y_position + inline_img_size[1]], 
                             outline=text_color, width=2)
        
        y_position += inline_img_size[1] + 20
    elif add_image:
        # Just one image - can use more space
        if os.path.exists(add_image):
            try:
                inline1 = Image.open(add_image).resize(inline_img_size)
                img.paste(inline1, (x_margin, y_position))
            except:
                draw.rectangle([x_margin, y_position, 
                              x_margin + inline_img_size[0], 
                              y_position + inline_img_size[1]], 
                             outline=text_color, width=2)
    elif add_image_2:
        # Just the second image - can use more space
        if os.path.exists(add_image_2):
            try:
                inline2 = Image.open(add_image_2).resize(inline_img_size)
                img.paste(inline2, (x_margin, y_position))
            except:
                draw.rectangle([x_margin, y_position, 
                              x_margin + inline_img_size[0], 
                              y_position + inline_img_size[1]], 
                             outline=text_color, width=2)
    
    # Draw logo
    logo_positions = {
        "top-left": (20, 20),
        "top-right": (img_size[0] - logo_size[0] - 20, 20),
        "bottom-left": (20, img_size[1] - logo_size[1] - 20),
        "bottom-right": (img_size[0] - logo_size[0] - 20, img_size[1] - logo_size[1] - 20)
    }
    
    if logo_path and logo_position in logo_positions and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).resize(logo_size)
            pos = logo_positions[logo_position]
            img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)
        except Exception as e:
            print(f"Warning: Could not load logo {logo_path}: {e}")
    
    # Save the image
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    img.save(output_path)


def setup_dummy_assets():
    """Create dummy logos and inline images if they don't exist."""
    print("Setting up dummy assets...")
    
    # Create dummy logos
    for i, logo_file in enumerate(logo_path):
        color = ["#FF6B6B", "#4ECDC4", "#45B7D1"][i % 3]
        create_dummy_image(logo_file, logo_size, color, f"LOGO {i+1}")
    
    # Create dummy inline images
    for i, img_file in enumerate(inline_img):
        color = ["#95E1D3", "#F38181", "#AA96DA"][i % 3]
        create_dummy_image(img_file, (300, 200), color, f"IMG {i+1}")
    
    print("Dummy assets created!\n")


def save_dataset_info(output_dir, image_pairs, style_labels, font_labels, config):
    """Save dataset metadata to a JSON file."""
    metadata = {
        "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "num_samples": len(image_pairs),
        "configuration": config,
        "dataset": []
    }
    
    for idx, (pair, style_label, font_label) in enumerate(zip(image_pairs, style_labels, font_labels)):
        metadata["dataset"].append({
            "pair_id": idx,
            "img1": pair[0],
            "img2": pair[1],
            "style_label": style_label,
            "font_label": font_label,
            "style_match": "identical" if style_label == 1 else "different",
            "font_match": "same" if font_label == 1 else "different"
        })
    
    metadata_path = os.path.join(output_dir, "dataset_metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\nDataset metadata saved to: {metadata_path}")


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Main function to generate the dataset."""
    print("=" * 70)
    print("PRESENTATION STYLE DATASET GENERATOR")
    print("=" * 70)
    print()
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print()
    
    # Setup dummy assets
    setup_dummy_assets()
    
    # Configuration info
    config = {
        "num_samples": NUM_SAMPLES,
        "table_min_rows": TABLE_MIN_ROWS,
        "table_max_rows": TABLE_MAX_ROWS,
        "table_min_cols": TABLE_MIN_COLS,
        "table_max_cols": TABLE_MAX_COLS,
        "image_size": img_size,
        "fonts": font_list,
        "background_colors": background_colors,
        "text_colors": text_colors
    }
    
    print("Configuration:")
    print(f"  - Number of samples: {NUM_SAMPLES}")
    print(f"  - Table rows: {TABLE_MIN_ROWS}-{TABLE_MAX_ROWS}")
    print(f"  - Table columns: {TABLE_MIN_COLS}-{TABLE_MAX_COLS}")
    print(f"  - Image size: {img_size[0]}x{img_size[1]}")
    print()
    
    # Generate dataset
    print("Generating dataset...")
    print("-" * 70)
    
    image_pairs, style_labels, font_labels = create_balanced_dataset(
        dataset_directory=OUTPUT_DIR,
        num_samples=NUM_SAMPLES,
        table_min_rows=TABLE_MIN_ROWS,
        table_max_rows=TABLE_MAX_ROWS,
        table_min_cols=TABLE_MIN_COLS,
        table_max_cols=TABLE_MAX_COLS,
        generate_image=generate_image
    )
    
    print("-" * 70)
    print()
    
    # Print statistics
    print("Dataset Statistics:")
    print(f"  - Total pairs generated: {len(image_pairs)}")
    print(f"  - Style labels: {sum(style_labels)} identical, {len(style_labels) - sum(style_labels)} different")
    print(f"  - Font labels: {sum(font_labels)} same, {len(font_labels) - sum(font_labels)} different")
    print()
    
    # Save metadata
    save_dataset_info(OUTPUT_DIR, image_pairs, style_labels, font_labels, config)
    
    print("=" * 70)
    print("DATASET GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\nCheck the '{OUTPUT_DIR}' folder for your generated images.")
    print(f"Total files created: {len(image_pairs) * 2} images")
    print()


if __name__ == "__main__":
    main()

