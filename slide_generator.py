"""
Slide generation module for creating presentation-style images.
Handles image rendering, text layout, tables, logos, and inline images.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont


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


def setup_dummy_assets(logo_paths, logo_size, inline_img_paths):
    """
    Create dummy logos and inline images if they don't exist.
    
    Args:
        logo_paths: List of logo file paths
        logo_size: Size tuple for logos (width, height)
        inline_img_paths: List of inline image file paths
    """
    print("Setting up dummy assets...")
    
    for i, logo_file in enumerate(logo_paths):
        if not os.path.exists(logo_file):
            color = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#95E1D3", "#F38181", "#AA96DA"][i % 6]
            create_dummy_image(logo_file, logo_size, color, f"LOGO {i+1}")
    
    for i, img_file in enumerate(inline_img_paths):
        if not os.path.exists(img_file):
            color = ["#95E1D3", "#F38181", "#AA96DA", "#FFD93D", "#6BCB77"][i % 5]
            create_dummy_image(img_file, (300, 200), color, f"IMG {i+1}")
    
    print("Dummy assets ready!\n")


def create_complex_images(
    dataset_directory,
    num_samples=50,
    llm_generator=None,
    config=None
):
    """
    Creates a dataset of COMPLEX images only - all features always enabled.
    
    Args:
        dataset_directory: Directory where images will be saved
        num_samples: Number of images to generate
        llm_generator: LLMTextGenerator instance for text generation
        config: Dictionary containing configuration:
            - img_size: Tuple (width, height) for image dimensions
            - logo_size: Tuple (width, height) for logo dimensions
            - font_list: List of font paths
            - background_colors: List of background color hex codes
            - text_colors: List of text color hex codes
            - border_color: Border color hex code
            - border: List of border widths
            - logo_path: List of logo file paths
            - logo_position: List of logo positions
            - inline_img: List of inline image file paths
            - table_borders: List of table border widths
            - table_border_colors: List of table border color hex codes
            - table_min_rows: Minimum table rows
            - table_max_rows: Maximum table rows
            - table_min_cols: Minimum table columns
            - table_max_cols: Maximum table columns
            - generate_presentation_text: Boolean to enable presentation text generation
            - use_llm: Boolean indicating if LLM is enabled
            - presentation_text_max_length: Maximum length of presentation text
    
    Returns:
        Tuple of (images, presentation_texts, full_data):
        - images: List of image file paths
        - presentation_texts: List of presentation text strings
        - full_data: List of dictionaries with image metadata
    """
    if config is None:
        raise ValueError("config parameter is required")
    
    # Extract configuration values
    img_size = config.get('img_size', (224, 224))
    logo_size = config.get('logo_size', (20, 20))
    font_list = config.get('font_list', [])
    background_colors = config.get('background_colors', [])
    text_colors = config.get('text_colors', [])
    border_color = config.get('border_color', "#000000")
    border = config.get('border', [2, 3, 4, 5])
    logo_path = config.get('logo_path', [])
    logo_position = config.get('logo_position', [])
    inline_img = config.get('inline_img', [])
    table_borders = config.get('table_borders', [2, 3, 4])
    table_border_colors = config.get('table_border_colors', [])
    table_min_rows = config.get('table_min_rows', 2)
    table_max_rows = config.get('table_max_rows', 4)
    table_min_cols = config.get('table_min_cols', 2)
    table_max_cols = config.get('table_max_cols', 4)
    generate_presentation_text = config.get('generate_presentation_text', False)
    use_llm = config.get('use_llm', True)
    presentation_text_max_length = config.get('presentation_text_max_length', 400)
    
    images = []
    presentation_texts = []
    full_data = []
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

        # Generate meaningful text (always 3 lines for complex images)
        # Title, bullet point 1, bullet point 2
        # Generate title first, then use it as context for bullets
        if llm_generator:
            title = llm_generator.generate_title()
            bullet1 = llm_generator.generate_bullet_point(title=title)
            bullet2 = llm_generator.generate_bullet_point(title=title)
        else:
            # Fallback if no LLM generator provided
            title = "Sample Title"
            bullet1 = "Sample bullet point 1"
            bullet2 = "Sample bullet point 2"
        
        texts = [title, bullet1, bullet2]
        line_spacing = random.choice([1, 2])
        border_status = True  # Always enabled

        # Always use 2 images for complex images
        add_image = random.choice(inline_img)
        add_image_2 = random.choice([img for img in inline_img if img != add_image])

        # Generate larger table data with meaningful content
        num_rows = random.randint(table_min_rows, table_max_rows)
        num_cols = random.randint(table_min_cols, table_max_cols)
        
        # Generate meaningful table headers and data
        if llm_generator:
            table_headers = llm_generator.generate_table_headers(num_cols)
            # Generate table data
            table_data = []
            for row in range(num_rows):
                row_data = []
                for col_idx, header in enumerate(table_headers):
                    value = llm_generator.generate_table_cell_data(header, row + 1)
                    row_data.append(value)
                table_data.append(row_data)
        else:
            # Fallback if no LLM generator provided
            table_headers = [f"Header {j+1}" for j in range(num_cols)]
            table_data = [[f"Data {i+1}-{j+1}" for j in range(num_cols)] for i in range(num_rows)]

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
        
        # Generate presentation text AFTER image creation by analyzing the image
        presentation_text = ""
        if generate_presentation_text:
            if not use_llm or not llm_generator:
                print(f"Warning: GENERATE_PRESENTATION_TEXT requires USE_LLM=True and llm_generator")
                presentation_text = f"Presentation about this slide (LLM disabled)"
            else:
                try:
                    # Use vision model to analyze the actual generated image
                    print(f"\nGenerating presentation text for img1_{i}.png...")
                    presentation_text = llm_generator.generate_presentation_text_from_image(
                        image_path=img_1_path,
                        max_length=presentation_text_max_length
                    )

                    if presentation_text and "analysis unavailable" not in presentation_text.lower() and "disabled" not in presentation_text.lower() and "api key" not in presentation_text.lower():
                        print(f"✓ Successfully generated presentation text for img1_{i}.png")
                        print(f"  Text: {presentation_text[:100]}..." if len(presentation_text) > 100 else f"  Text: {presentation_text}")
                    else:
                        # Vision failed or not supported - use content-based generation
                        if not presentation_text:
                            print(f"Note: Using content-based text generation (vision not available or failed)...")
                        else:
                            print(f"⚠ Warning: Vision analysis failed, generating text from slide content...")
                        # Generate meaningful presentation text based on slide content
                        try:
                            presentation_text = llm_generator.generate_presentation_text_from_content(
                                title=texts[0],
                                bullet_points=[texts[1], texts[2]],
                                table_headers=table_headers,
                                max_length=presentation_text_max_length
                            )
                            
                            if presentation_text and "analysis unavailable" not in presentation_text.lower() and "disabled" not in presentation_text.lower():
                                print(f"✓ Generated presentation text from slide content ({len(presentation_text)} chars)")
                            else:
                                print(f"  Fallback generation returned error text")
                        except Exception as e2:
                            print(f"  Fallback generation also failed: {e2}")
                            # Last resort: create a simple description from available content
                            presentation_text = f"This slide presents {texts[0].lower()}. Key highlights include {texts[1].lower()} and {texts[2].lower()}. The slide also contains a data table with {', '.join(table_headers)}."
                            if len(presentation_text) > presentation_text_max_length:
                                presentation_text = presentation_text[:presentation_text_max_length - 3] + "..."
                            print(f"✓ Generated basic presentation text from slide content")
                except Exception as e:
                    print(f"✗ Error: Failed to generate presentation text from image: {e}")
                    import traceback
                    traceback.print_exc()
                    # Try to generate a basic text description from slide content
                    try:
                        presentation_text = f"This slide presents {texts[0].lower()}. Key highlights include {texts[1].lower()} and {texts[2].lower()}. The slide also contains a data table with {', '.join(table_headers)}."
                        if len(presentation_text) > presentation_text_max_length:
                            presentation_text = presentation_text[:presentation_text_max_length - 3] + "..."
                        print(f"✓ Generated basic presentation text from slide content")
                    except:
                        presentation_text = f"Presentation about this slide (image analysis failed)"
        else:
            presentation_text = f"Presentation about this slide (disabled)"
        
        images.append(img_1_path)
        presentation_texts.append(presentation_text)
        temp_dict = {'img_path': 'img_1_path', 'text': presentation_text, 'in-sync': 1}
        full_data.append(temp_dict)
        i += 1
    
    return images, presentation_texts, full_data
