import random
from collections import Counter

# Default configuration values
# These can be overridden by setting them globally before importing or calling functions
DEFAULT_FONT_LIST = [
    "C:\\Windows\\Fonts\\arial.ttf",
    "C:\\Windows\\Fonts\\arialbd.ttf",          # Arial Bold
    "C:\\Windows\\Fonts\\times.ttf",
    "C:\\Windows\\Fonts\\timesbd.ttf",          # Times New Roman Bold
    "C:\\Windows\\Fonts\\verdana.ttf",
    "C:\\Windows\\Fonts\\verdanab.ttf",         # Verdana Bold
    "C:\\Windows\\Fonts\\calibri.ttf",
    "C:\\Windows\\Fonts\\calibrib.ttf",         # Calibri Bold
    "C:\\Windows\\Fonts\\georgia.ttf",
    "C:\\Windows\\Fonts\\georgiab.ttf",         # Georgia Bold
    "C:\\Windows\\Fonts\\tahoma.ttf",
    "C:\\Windows\\Fonts\\tahomabd.ttf",         # Tahoma Bold
    "C:\\Windows\\Fonts\\trebuc.ttf",           # Trebuchet MS
    "C:\\Windows\\Fonts\\trebucbd.ttf",         # Trebuchet MS Bold
    "C:\\Windows\\Fonts\\comic.ttf",            # Comic Sans MS
    "C:\\Windows\\Fonts\\comicbd.ttf",          # Comic Sans MS Bold
    "C:\\Windows\\Fonts\\corbel.ttf",
    "C:\\Windows\\Fonts\\corbelb.ttf",          # Corbel Bold
    "C:\\Windows\\Fonts\\consola.ttf",          # Consolas
    "C:\\Windows\\Fonts\\consolab.ttf"          # Consolas Bold
]

DEFAULT_BACKGROUND_COLORS = [
    "#FFFFFF",  # Pure White
    "#FAFAFA",  # Off White
    "#F5F5F5",  # Light Gray 1
    "#F0F0F0",  # Light Gray 2
    "#E8E8E8",  # Light Gray 3
    "#E0E0E0",  # Light Gray 4
    "#D3D3D3",  # Light Gray 5
    "#FFF8DC",  # Cornsilk (Warm White)
    "#F5F5DC",  # Beige
    "#FDF5E6",  # Old Lace (Cream)
    "#FAF0E6",  # Linen
    "#F0F8FF",  # Alice Blue (Cool White)
    "#F8F8FF",  # Ghost White
    "#FFFAF0",  # Floral White
    "#FFF5EE"   # Seashell
]

DEFAULT_TEXT_COLORS = [
    "#000000",  # Pure Black
    "#0A0A0A",  # Near Black 1
    "#141414",  # Near Black 2
    "#1a1a1a",  # Near Black 3
    "#1F1F1F",  # Near Black 4
    "#262626",  # Dark Gray 1
    "#2c2c2c",  # Dark Gray 2
    "#333333",  # Dark Gray 3
    "#3D3D3D",  # Dark Gray 4
    "#404040",  # Dark Gray 5
    "#4d4d4d",  # Medium Dark Gray 1
    "#525252",  # Medium Dark Gray 2
    "#595959",  # Medium Dark Gray 3
    "#666666",  # Medium Dark Gray 4
    "#1C1C1C"   # Charcoal
]

DEFAULT_BORDER = [1, 2, 3, 4]
DEFAULT_BORDER_COLOR = "#000000"
DEFAULT_LOGO_PATH = ["OIP.png", "OIP (1).png", "OIP (2).png", "OIP (3).png", "OIP (4).png", "OIP (5).png"]
DEFAULT_LOGO_POSITION = ["top-left", "top-right", "bottom-left", "bottom-right"]
DEFAULT_INLINE_IMG = ["pres2.png", "pres3.png", "pres4.png", "pres5.png", "pres6.png"]
DEFAULT_TABLE_BORDERS = [1, 2, 3, 4]
DEFAULT_TABLE_BORDER_COLORS = [
    "#000000",  # Black
    "#1a1a1a",  # Near Black
    "#262626",  # Dark Gray 1
    "#333333",  # Dark Gray 2
    "#404040",  # Dark Gray 3
    "#4d4d4d",  # Medium Dark Gray 1
    "#555555",  # Medium Dark Gray 2
    "#595959",  # Medium Dark Gray 3
    "#666666",  # Medium Gray 1
    "#6B6B6B",  # Medium Gray 2
    "#707070",  # Medium Gray 3
    "#777777",  # Medium Gray 4
    "#808080",  # Gray
    "#8B8B8B",  # Light Gray 1
    "#999999"   # Light Gray 2
]
DEFAULT_IMG_SIZE = (1024, 768)
DEFAULT_LOGO_SIZE = (120, 120)


def generate_random_text(num_words=None, min_word_length=2, max_word_length=12):
    """
    Generates random text with varying length using random letters.
    
    Args:
        num_words: Number of words to generate. If None, generates random number (1-10)
        min_word_length: Minimum length of each word (default: 2)
        max_word_length: Maximum length of each word (default: 12)
    
    Returns:
        String of random words separated by spaces
    """
    import string
    
    # If num_words not specified, choose randomly based on text length category
    if num_words is None:
        length_type = random.randint(1, 6)
        
        if length_type == 1:
            # Very short: 1 word
            num_words = 1
        elif length_type == 2:
            # Short: 1-2 words
            num_words = random.randint(1, 2)
        elif length_type == 3:
            # Medium-short: 2-4 words
            num_words = random.randint(2, 4)
        elif length_type == 4:
            # Medium: 3-6 words
            num_words = random.randint(3, 6)
        elif length_type == 5:
            # Long: 5-8 words
            num_words = random.randint(5, 8)
        else:
            # Very long: 7-10 words
            num_words = random.randint(7, 10)
    
    # Generate the specified number of random words
    text_parts = []
    
    for _ in range(num_words):
        # Random word length
        word_length = random.randint(min_word_length, max_word_length)
        
        # Generate random word
        word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        
        # Capitalize first letter sometimes (50% chance)
        if random.random() < 0.5:
            word = word.capitalize()
        
        text_parts.append(word)
    
    return ' '.join(text_parts)


def generate_table_data(num_rows=3, num_cols=3, use_random_text=True):
    """
    Generates random table data.
    
    Args:
        num_rows: Number of data rows in the table
        num_cols: Number of columns in the table
        use_random_text: If True, uses random letters. If False, uses numbered format
    
    Returns:
        Tuple of (headers, data) where headers is a list and data is a list of lists
    """
    if use_random_text:
        # Generate random text headers (1-2 words each)
        headers = [generate_random_text(num_words=random.randint(1, 2), min_word_length=3, max_word_length=8) 
                   for _ in range(num_cols)]
        
        # Generate random text data (1-3 words per cell)
        data = []
        for row in range(num_rows):
            row_data = [generate_random_text(num_words=random.randint(1, 3), min_word_length=2, max_word_length=10) 
                       for col in range(num_cols)]
            data.append(row_data)
    else:
        # Use simple numbered format
        headers = [f"Column {i+1}" for i in range(num_cols)]
        data = []
        for row in range(num_rows):
            row_data = [f"Data {row+1}-{col+1}" for col in range(num_cols)]
            data.append(row_data)
    
    return headers, data

def create_balanced_dataset(dataset_directory, num_samples=50, table_min_rows=2, table_max_rows=5, table_min_cols=2, table_max_cols=4, include_tables=True, table_probability=0.3, generate_image=None):
    """
    Generates a dataset with 50% identical pairs and 50% pairs differing by one attribute,
    with variations in text quantity, images, and border configurations.
    Each slide randomly decides whether to include logos, tables, and bullets independently.
    
    Args:
        dataset_directory: Path to save generated images
        num_samples: Number of image pairs to generate
        table_min_rows: Minimum number of rows in tables (default: 2)
        table_max_rows: Maximum number of rows in tables (default: 5)
        table_min_cols: Minimum number of columns in tables (default: 2)
        table_max_cols: Maximum number of columns in tables (default: 4)
        include_tables: Whether to allow tables in generated images (default: True)
        table_probability: Deprecated - table inclusion is now per-slide (50% chance each)
        generate_image: Function to generate individual images (if None, will try to get from globals)
    """
    # Placeholder lists for storing results
    image_pairs = []
    style_labels = []
    font_labels = []

    # Target number of samples for each label (0s and 1s)
    target_per_class = num_samples // 2

    # Counters for label balancing
    style_label_count = Counter({0: 0, 1: 0})

    i = 0  # Counter for image naming

    # Use provided global variables or fall back to defaults
    font_list = globals().get('font_list', DEFAULT_FONT_LIST)
    background_colors = globals().get('background_colors', DEFAULT_BACKGROUND_COLORS)
    text_colors = globals().get('text_colors', DEFAULT_TEXT_COLORS)
    border = globals().get('border', DEFAULT_BORDER)
    border_color = globals().get('border_color', DEFAULT_BORDER_COLOR)
    logo_path = globals().get('logo_path', DEFAULT_LOGO_PATH)
    logo_position = globals().get('logo_position', DEFAULT_LOGO_POSITION)
    inline_img = globals().get('inline_img', DEFAULT_INLINE_IMG)
    table_borders = globals().get('table_borders', DEFAULT_TABLE_BORDERS)
    table_border_colors = globals().get('table_border_colors', DEFAULT_TABLE_BORDER_COLORS)
    img_size = globals().get('img_size', DEFAULT_IMG_SIZE)
    logo_size = globals().get('logo_size', DEFAULT_LOGO_SIZE)
    
    # Check if generate_image function is defined (use parameter first, then globals)
    if generate_image is None:
        generate_image = globals().get('generate_image')
    if generate_image is None:
        raise NameError(
            "generate_image function is not defined. "
            "Please pass it as a parameter to create_balanced_dataset() "
            "or define it globally before calling create_balanced_dataset() "
            "or use main.py which includes the full implementation."
        )

    # Keep generating images until we have exactly `num_samples` pairs
    while len(image_pairs) < num_samples:
        # Decide whether the images will be identical or differ by one attribute
        is_same = random.random() < 0.5

        if is_same and style_label_count[1] < target_per_class:
            # Identical attributes
            font_1 = font_2 = random.choice(font_list)
            bg_color_1 = bg_color_2 = random.choice(background_colors)
            text_color_1 = text_color_2 = random.choice(text_colors)
            border_1 = border_2 = random.choice(border)
            has_logo_1 = has_logo_2 = random.choice([True, False])
            logo_path_1 = logo_path_2 = random.choice(logo_path) if has_logo_1 else None
            logo_position1 = logo_position2 = random.choice(logo_position)
            has_bullets_1 = has_bullets_2 = random.choice([True, False])
            has_table_1 = has_table_2 = random.choice([True, False])
            table_border_1 = table_border_2 = random.choice(table_borders)
            table_border_color_1 = table_border_color_2 = random.choice(table_border_colors)
            style_label = 1
        elif not is_same and style_label_count[0] < target_per_class:
            # Differing attributes
            style_label = 0
            font_1 = random.choice(font_list)
            font_2 = font_1 if random.random() < 0.5 else random.choice(font_list)
            bg_color_1 = random.choice(background_colors)
            bg_color_2 = bg_color_1 if random.random() < 0.5 else random.choice(background_colors)
            text_color_1 = random.choice(text_colors)
            text_color_2 = text_color_1 if random.random() < 0.5 else random.choice(text_colors)
            border_1 = random.choice(border)
            border_2 = border_1 if random.random() < 0.5 else random.choice(border)
            has_logo_1 = random.choice([True, False])
            has_logo_2 = has_logo_1 if random.random() < 0.5 else random.choice([True, False])
            logo_path_1 = random.choice(logo_path) if has_logo_1 else None
            logo_path_2 = (logo_path_1 if logo_path_1 and random.random() < 0.5 else random.choice(logo_path)) if has_logo_2 else None
            logo_position1 = random.choice(logo_position)
            logo_position2 = random.choice(logo_position)
            has_bullets_1 = random.choice([True, False])
            has_bullets_2 = has_bullets_1 if random.random() < 0.5 else random.choice([True, False])
            has_table_1 = random.choice([True, False])
            has_table_2 = has_table_1 if random.random() < 0.5 else random.choice([True, False])
            table_border_1 = random.choice(table_borders)
            table_border_2 = table_border_1 if random.random() < 0.5 else random.choice(table_borders)
            table_border_color_1 = random.choice(table_border_colors)
            table_border_color_2 = table_border_color_1 if random.random() < 0.5 else random.choice(table_border_colors)
        else:
            continue

        # Generate random text (1-3 lines)
        texts = [generate_random_text() for _ in range(random.randint(1, 3))]
        line_spacing = random.choice([1, 2])
        border_status = random.choice([True, False])

        # Determine add_image value: random choice from inline_img if adding an image
        add_image = random.choice(inline_img) if random.random() < 0.3 else None
        
        # Determine if a second image should be added (30% chance)
        add_image_2 = random.choice(inline_img) if random.random() < 0.3 else None

        # Generate table data if either slide needs a table (based on include_tables parameter)
        if include_tables and (has_table_1 or has_table_2):
            num_rows = random.randint(table_min_rows, table_max_rows)
            num_cols = random.randint(table_min_cols, table_max_cols)
            table_headers, table_data = generate_table_data(num_rows, num_cols)
        else:
            table_headers = None
            table_data = None

        # Generate the two images with specified attributes
        img_1_path = f"{dataset_directory}\\img1_{i}.png"
        img_2_path = f"{dataset_directory}\\img2_{i}.png"
        i += 1

        generate_image(
            font_path=font_1,
            img_background_color=bg_color_1,
            output_path=img_1_path,
            text_color=text_color_1,
            img_size=img_size,
            font_size=random.choice((16, 18, 20)),
            title_font_size=random.choice((32, 36, 40)),
            line_spacing=line_spacing,
            logo_size=logo_size,
            border=border_status,
            border_color=border_color,
            border_width=border_1,
            logo_path=logo_path_1,
            logo_position=logo_position1,
            add_image=add_image,
            add_image_2=add_image_2,
            title=texts[0] if len(texts) > 0 else None,
            text1=texts[1] if len(texts) > 1 else None,
            text2=texts[2] if len(texts) > 2 else None,
            bullet=has_bullets_1,
            add_table=has_table_1,
            table_headers=table_headers,
            table_data=table_data,
            table_border=table_border_1,
            table_border_color=table_border_color_1
        )
        generate_image(
            font_path=font_2,
            img_background_color=bg_color_2,
            output_path=img_2_path,
            text_color=text_color_2,
            img_size=img_size,
            font_size=random.choice((16, 18, 20)),
            title_font_size=random.choice((32, 36, 40)),
            line_spacing=line_spacing,
            logo_size= logo_size,
            border=border_status,
            border_color=border_color,
            border_width=border_2,
            logo_path=logo_path_2,
            logo_position=logo_position2,
            add_image=add_image,
            add_image_2=add_image_2,
            title=texts[0] if len(texts) > 0 else None,
            text1=texts[1] if len(texts) > 1 else None,
            text2=texts[2] if len(texts) > 2 else None,
            bullet=has_bullets_2,
            add_table=has_table_2,
            table_headers=table_headers,
            table_data=table_data,
            table_border=table_border_2,
            table_border_color=table_border_color_2
        )

        font_label = 1 if font_1 == font_2 else 0

        # Append image paths and labels
        image_pairs.append((img_1_path, img_2_path))
        style_labels.append(style_label)
        font_labels.append(font_label)

        # Update counters
        style_label_count[style_label] += 1

    return image_pairs, style_labels, font_labels
