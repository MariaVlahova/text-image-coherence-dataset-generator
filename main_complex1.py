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
from PIL import Image, ImageDraw, ImageFont
from datasetGenaratorPStyle import create_balanced_dataset, generate_table_data, generate_random_text
import json
from datetime import datetime


# ============================================================
# CONFIGURATION - Complex Images Only
# ============================================================

# Dataset settings
NUM_SAMPLES = 50  # Number of image pairs to generate
OUTPUT_DIR = "data_complex1"  # Subfolder where dataset will be saved

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
logo_path = ["OIP.png", "OIP (1).png", "OIP (2).png", "OIP (3).png", "OIP (4).png", "OIP (5).png"]
logo_position = ["top-left", "top-right", "bottom-left", "bottom-right"]

# Inline image settings - always use 2 images
inline_img = ["pres2.png", "pres3.png", "pres4.png", "pres5.png", "pres6.png"]

# Table settings - thicker borders
table_borders = [2, 3, 4]
table_border_colors = [
    "#000000", "#1a1a1a", "#262626", "#333333", "#404040",
    "#4d4d4d", "#555555", "#595959", "#666666"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def wrap_text_by_words(text, draw, font, max_width):
    """
    Wraps text into multiple lines without splitting words.
    """
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines if lines else [text]


def create_dummy_image(path, size=(200, 150), color="#4A90E2", label="IMAGE"):
    """Creates a dummy placeholder image."""
    if not os.path.exists(path):
        img = Image.new('RGB', size, color=color)
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([0, 0, size[0]-1, size[1]-1], outline="#FFFFFF", width=3)
        
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
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
    Generates a COMPLEX presentation slide image with ALL features enabled.
    """
    # Create a new image
    img = Image.new('RGB', img_size, color=img_background_color)
    draw = ImageDraw.Draw(img)
    
    # Add border (always enabled for complex images)
    if border:
        for i in range(border_width):
            draw.rectangle([i, i, img_size[0]-1-i, img_size[1]-1-i], 
                         outline=border_color, width=1)
    
    # Load fonts - larger for readability in 224x224 images
    try:
        title_font = ImageFont.truetype(font_path, title_font_size)
        text_font = ImageFont.truetype(font_path, font_size)
        # Table font should be smaller than body text but still readable
        table_font_size = max(8, int(font_size * 0.8))
        small_font = ImageFont.truetype(font_path, table_font_size)
    except Exception as e:
        print(f"Warning: Could not load font {font_path}, using default. Error: {e}")
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Calculate initial y_position - scaled for 224x224 images
    base_y_position = 15 + border_width * 2
    x_margin = 10 + border_width * 2
    
    # Track content areas to prevent logo overlap
    content_areas = []  # List of (x, y, width, height) tuples
    
    # Check if logo is in top position and adjust y_position
    top_logo_y = None
    if logo_path and logo_position in ["top-left", "top-right"] and os.path.exists(logo_path):
        logo_bottom = 5 + logo_size[1]
        y_position = max(base_y_position, logo_bottom + 3)
        # Track top logo area
        if logo_position == "top-left":
            top_logo_y = (5, 5, logo_size[0], logo_size[1])
        else:  # top-right
            top_logo_y = (img_size[0] - logo_size[0] - 5, 5, logo_size[0], logo_size[1])
    else:
        y_position = base_y_position
    
    # Draw title with word wrapping (always present in complex images) - MAX 2 ROWS
    if title:
        if logo_path and logo_position in ["top-right"] and os.path.exists(logo_path):
            max_title_width = img_size[0] - x_margin - logo_size[0] - 5
        elif logo_path and logo_position in ["top-left"] and os.path.exists(logo_path):
            max_title_width = img_size[0] - 2 * x_margin
        else:
            max_title_width = img_size[0] - 2 * x_margin
        
        title_lines = wrap_text_by_words(title, draw, title_font, max_title_width)
        
        # Limit to maximum 2 rows
        if len(title_lines) > 2:
            # Take first line, truncate second line if needed
            first_line = title_lines[0]
            # Try to fit as much of second line as possible, add "..." if needed
            second_line_text = ' '.join(title_lines[1:])  # Combine all remaining lines
            # Check if second line fits
            bbox = draw.textbbox((0, 0), second_line_text, font=title_font)
            text_width = bbox[2] - bbox[0]
            if text_width > max_title_width:
                # Truncate second line character by character
                truncated = second_line_text
                while len(truncated) > 1:
                    test_text = truncated + "..."
                    bbox = draw.textbbox((0, 0), test_text, font=title_font)
                    if bbox[2] - bbox[0] <= max_title_width:
                        second_line = test_text
                        break
                    truncated = truncated[:-1]
                else:
                    # If even with ellipsis it doesn't fit, use just "..."
                    second_line = "..."
            else:
                second_line = second_line_text
            title_lines = [first_line, second_line]
        elif len(title_lines) == 0:
            title_lines = [title]  # Fallback if wrapping fails
        
        # Track title area
        title_start_y = y_position
        title_end_y = y_position
        
        # Draw title lines (max 2)
        for i, line in enumerate(title_lines[:2]):  # Ensure max 2 lines
            draw.text((x_margin, y_position), line, fill=text_color, font=title_font)
            y_position += title_font_size + line_spacing * 2
            title_end_y = y_position
        
        y_position += line_spacing * 2
        
        # Draw separator line
        line_y = y_position + 2
        line_start_x = x_margin
        line_end_x = img_size[0] - x_margin
        draw.line([(line_start_x, line_y), (line_end_x, line_y)], 
                 fill=text_color, width=1)
        y_position = line_y + 4
        
        # Record title area
        content_areas.append((x_margin, title_start_y, img_size[0] - 2 * x_margin, title_end_y - title_start_y))
    
    # Draw text1 (always present with bullets in complex images)
    if text1:
        prefix = "• " if bullet else ""
        bullet_indent = 5 if bullet else 0
        text1_y = y_position
        draw.text((x_margin + bullet_indent, y_position), 
                 f"{prefix}{text1}", fill=text_color, font=text_font)
        y_position += font_size + line_spacing * 3
        content_areas.append((x_margin, text1_y, img_size[0] - 2 * x_margin, font_size))
    
    # Draw text2 (always present with bullets in complex images)
    if text2:
        prefix = "• " if bullet else ""
        bullet_indent = 5 if bullet else 0
        text2_y = y_position
        draw.text((x_margin + bullet_indent, y_position), 
                 f"{prefix}{text2}", fill=text_color, font=text_font)
        y_position += font_size + line_spacing * 3
        content_areas.append((x_margin, text2_y, img_size[0] - 2 * x_margin, font_size))
    
    y_position += 4
    
    # Draw table (always enabled in complex images) - scaled for 224x224
    if add_table and table_headers and table_data:
        table_x = x_margin
        table_y = y_position
        table_width = min(200, img_size[0] - 2 * x_margin)  # Fit in 224px width
        
        num_cols = len(table_headers)
        num_rows = len(table_data)
        cell_width = table_width // num_cols
        cell_height = 18  # Slightly taller cells for better readability
        
        table_height = (num_rows + 1) * cell_height
        # Table border
        draw.rectangle([table_x, table_y, table_x + table_width, table_y + table_height],
                      outline=table_border_color, width=max(1, table_border))
        
        # Helper function to truncate text to fit cell width - ensures no overflow
        def truncate_text(text, max_width, font):
            """Truncate text to fit within max_width pixels, ensuring no overflow."""
            if not text:
                return ""
            text_str = str(text)
            # Test if text fits
            bbox = draw.textbbox((0, 0), text_str, font=font)
            text_width = bbox[2] - bbox[0]
            if text_width <= max_width:
                return text_str
            # Truncate character by character until it fits
            truncated = text_str
            # Try with ellipsis first
            while len(truncated) > 0:
                test_text = truncated + "..." if len(truncated) < len(text_str) else truncated
                bbox = draw.textbbox((0, 0), test_text, font=font)
                if bbox[2] - bbox[0] <= max_width:
                    return test_text
                if len(truncated) <= 1:
                    break
                truncated = truncated[:-1]
            # If even single char doesn't fit, return empty or minimal
            if len(truncated) == 0:
                return ""
            # Return just the first character if that's all that fits
            bbox = draw.textbbox((0, 0), truncated[0], font=font)
            if bbox[2] - bbox[0] <= max_width:
                return truncated[0]
            return ""
        
        # Draw headers
        for col_idx, header in enumerate(table_headers):
            cell_x = table_x + col_idx * cell_width
            draw.rectangle([cell_x, table_y, cell_x + cell_width, table_y + cell_height],
                         outline=table_border_color, width=max(1, table_border))
            # Truncate header text to fit - ensure no overflow
            max_text_width = max(5, cell_width - 4)  # Leave 2px padding on each side, minimum 5px
            truncated_header = truncate_text(header, max_text_width, small_font)
            # Center text vertically in cell
            bbox = draw.textbbox((0, 0), truncated_header, font=small_font)
            text_height = bbox[3] - bbox[1]
            text_y = table_y + (cell_height - text_height) // 2
            draw.text((cell_x + 2, text_y), truncated_header, 
                     fill=text_color, font=small_font)
        
        # Draw data rows
        for row_idx, row_data in enumerate(table_data):
            row_y = table_y + (row_idx + 1) * cell_height
            for col_idx, cell_data in enumerate(row_data):
                cell_x = table_x + col_idx * cell_width
                draw.rectangle([cell_x, row_y, cell_x + cell_width, row_y + cell_height],
                             outline=table_border_color, width=max(1, table_border))
                # Truncate cell text to fit - ensure no overflow
                max_text_width = max(5, cell_width - 4)  # Leave 2px padding on each side, minimum 5px
                truncated_cell = truncate_text(cell_data, max_text_width, small_font)
                # Center text vertically in cell
                bbox = draw.textbbox((0, 0), truncated_cell, font=small_font)
                text_height = bbox[3] - bbox[1]
                text_y = row_y + (cell_height - text_height) // 2
                draw.text((cell_x + 2, text_y), truncated_cell, 
                         fill=text_color, font=small_font)
        
        # Record table area
        content_areas.append((table_x, table_y, table_width, table_height))
        
        y_position += table_height + 4
    
    # Draw inline images - only if there's enough space for readable images
    min_readable_img_size = 30  # Minimum size for images to be readable/useful
    available_height = img_size[1] - y_position - 5
    
    if logo_path and logo_position in ["bottom-left", "bottom-right"] and os.path.exists(logo_path):
        available_height = img_size[1] - y_position - logo_size[1] - 8
    
    # Only draw images if we have enough space
    if available_height >= min_readable_img_size:
        available_width = img_size[0] - 2 * x_margin
        
        # Check if we have space for 2 images side by side
        if add_image and add_image_2:
            img_spacing = 4
            total_available_width = available_width - img_spacing
            single_img_width = total_available_width // 2
            single_img_height = min(available_height, single_img_width)
            
            # Only draw if images would be readable
            if single_img_width >= min_readable_img_size and single_img_height >= min_readable_img_size:
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
                                     outline=text_color, width=1)
                
                if os.path.exists(add_image_2):
                    try:
                        inline2 = Image.open(add_image_2).resize(inline_img_size)
                        img.paste(inline2, (img2_x, y_position))
                    except:
                        draw.rectangle([img2_x, y_position, 
                                      img2_x + inline_img_size[0], 
                                      y_position + inline_img_size[1]], 
                                     outline=text_color, width=1)
                
                # Record image areas
                content_areas.append((img1_x, y_position, inline_img_size[0], inline_img_size[1]))
                content_areas.append((img2_x, y_position, inline_img_size[0], inline_img_size[1]))
        # Check if we have space for a single image
        elif add_image:
            single_img_width = min(available_width, available_height)
            single_img_height = single_img_width
            
            # Only draw if image would be readable
            if single_img_width >= min_readable_img_size:
                inline_img_size = (single_img_width, single_img_height)
                
                if os.path.exists(add_image):
                    try:
                        inline1 = Image.open(add_image).resize(inline_img_size)
                        img.paste(inline1, (x_margin, y_position))
                    except:
                        draw.rectangle([x_margin, y_position, 
                                      x_margin + inline_img_size[0], 
                                      y_position + inline_img_size[1]], 
                                     outline=text_color, width=1)
                
                # Record image area
                content_areas.append((x_margin, y_position, inline_img_size[0], inline_img_size[1]))
        elif add_image_2:
            single_img_width = min(available_width, available_height)
            single_img_height = single_img_width
            
            # Only draw if image would be readable
            if single_img_width >= min_readable_img_size:
                inline_img_size = (single_img_width, single_img_height)
                
                if os.path.exists(add_image_2):
                    try:
                        inline2 = Image.open(add_image_2).resize(inline_img_size)
                        img.paste(inline2, (x_margin, y_position))
                    except:
                        draw.rectangle([x_margin, y_position, 
                                      x_margin + inline_img_size[0], 
                                      y_position + inline_img_size[1]], 
                                     outline=text_color, width=1)
                
                # Record image area
                content_areas.append((x_margin, y_position, inline_img_size[0], inline_img_size[1]))
    # If not enough space, skip images entirely (they won't be drawn)
    
    # Helper function to check if logo overlaps with content
    def logo_overlaps_content(logo_x, logo_y, logo_w, logo_h, content_areas):
        """Check if logo rectangle overlaps with any content area."""
        logo_right = logo_x + logo_w
        logo_bottom = logo_y + logo_h
        
        for (cx, cy, cw, ch) in content_areas:
            content_right = cx + cw
            content_bottom = cy + ch
            
            # Check for overlap
            if not (logo_right <= cx or logo_x >= content_right or 
                   logo_bottom <= cy or logo_y >= content_bottom):
                return True
        return False
    
    # Draw logo (always enabled in complex images) - scaled for 224x224
    # Only draw if it doesn't overlap with content
    logo_positions = {
        "top-left": (5, 5),
        "top-right": (img_size[0] - logo_size[0] - 5, 5),
        "bottom-left": (5, img_size[1] - logo_size[1] - 5),
        "bottom-right": (img_size[0] - logo_size[0] - 5, img_size[1] - logo_size[1] - 5)
    }
    
    if logo_path and logo_position in logo_positions and os.path.exists(logo_path):
        logo_pos = logo_positions[logo_position]
        logo_x, logo_y = logo_pos
        logo_w, logo_h = logo_size
        
        # Check if logo would overlap with content
        if not logo_overlaps_content(logo_x, logo_y, logo_w, logo_h, content_areas):
            try:
                logo = Image.open(logo_path).resize(logo_size)
                img.paste(logo, logo_pos, logo if logo.mode == 'RGBA' else None)
            except Exception as e:
                print(f"Warning: Could not load logo {logo_path}: {e}")
        # If logo would overlap, skip drawing it (silently)
    
    # Save the image
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    img.save(output_path)


def setup_dummy_assets():
    """Create dummy logos and inline images if they don't exist."""
    print("Setting up dummy assets...")
    
    for i, logo_file in enumerate(logo_path):
        if not os.path.exists(logo_file):
            color = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#95E1D3", "#F38181", "#AA96DA"][i % 6]
            create_dummy_image(logo_file, logo_size, color, f"LOGO {i+1}")
    
    for i, img_file in enumerate(inline_img):
        if not os.path.exists(img_file):
            color = ["#95E1D3", "#F38181", "#AA96DA", "#FFD93D", "#6BCB77"][i % 5]
            create_dummy_image(img_file, (300, 200), color, f"IMG {i+1}")
    
    print("Dummy assets ready!\n")





def save_dataset_info(output_dir, image_pairs, style_labels, font_labels, config):
    """Save dataset metadata to a JSON file."""
    metadata = {
        "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "num_samples": len(image_pairs),
        "complex_images": True,
        "all_features_enabled": True,
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
def create_complex_images(dataset_directory, num_samples=50, generate_image=None):
    """
    Creates a dataset of COMPLEX images only - all features always enabled.
    """
    images = []
    i = 0

    while i < num_samples:
        font_1 = random.choice(font_list)
        bg_color_1 = random.choice(background_colors)
        text_color_1 = random.choice(text_colors)
        border_1 = random.choice(border)
        logo_path_1 = random.choice(logo_path)
        logo_position1 = random.choice(logo_position)
        table_border_1 = random.choice(table_borders)
        table_border_color_1 = random.choice(table_border_colors)

        # Generate random text (always 3 lines for complex images)
        texts = [generate_random_text() for _ in range(3)]
        line_spacing = random.choice([1, 2])
        border_status = True  # Always enabled

        # Always use 2 images for complex images
        add_image = random.choice(inline_img)
        add_image_2 = random.choice([img for img in inline_img if img != add_image])

        # Generate larger table data with SHORTER text for 224x224 images
        num_rows = random.randint(TABLE_MIN_ROWS, TABLE_MAX_ROWS)
        num_cols = random.randint(TABLE_MIN_COLS, TABLE_MAX_COLS)
        # Generate table data with shorter text (single short words)
        table_headers = [generate_random_text(num_words=1, min_word_length=2, max_word_length=4) 
                        for _ in range(num_cols)]
        table_data = []
        for row in range(num_rows):
            row_data = [generate_random_text(num_words=1, min_word_length=2, max_word_length=4) 
                       for col in range(num_cols)]
            table_data.append(row_data)

        # Generate the image
        img_1_path = f"{dataset_directory}\\img1_{i}.png"

        generate_image(
            font_path=font_1,
            img_background_color=bg_color_1,
            output_path=img_1_path,
            text_color=text_color_1,
            img_size=img_size,
            font_size=random.choice((12, 14, 16)),
            title_font_size=random.choice((20, 22, 24)),
            line_spacing=line_spacing,
            logo_size=logo_size,
            border=border_status,
            border_color=border_color,
            border_width=border_1,
            logo_path=logo_path_1,
            logo_position=logo_position1,
            add_image=add_image,
            add_image_2=add_image_2,
            title=texts[0],
            text1=texts[1],
            text2=texts[2],
            bullet=True,  # Always enabled
            add_table=True,  # Always enabled
            table_headers=table_headers,
            table_data=table_data,
            table_border=table_border_1,
            table_border_color=table_border_color_1
        )
        i += 1

def main():
    """Main function to generate complex images dataset."""
    print("=" * 70)
    print("COMPLEX PRESENTATION STYLE DATASET GENERATOR")
    print("All features enabled: Tables, Logos, 2 Images, Bullets, Borders")
    print("=" * 70)
    print()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print()
    
    setup_dummy_assets()
    
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
    
    create_complex_images(
        dataset_directory=OUTPUT_DIR,
        num_samples=NUM_SAMPLES,
        generate_image=generate_image
    )

    print("=" * 70)
    print("COMPLEX DATASET GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\nCheck the '{OUTPUT_DIR}' folder for your generated images.")
    print(f"Total files created: 50 images")
    print()


if __name__ == "__main__":
    main()

