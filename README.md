# Presentation Style Dataset Generator

Generate balanced datasets of presentation slide images with varying style attributes for machine learning applications.

## 📦 Installation

### Option 1: Automatic Setup (Recommended)
```
1. Double-click: setup.bat
2. Wait for installation to complete
```

### Option 2: Manual Installation
```bash
pip install -r requirements.txt
```

### Option 3: Install Pillow Only
```bash
pip install Pillow
```

## 🚀 Quick Start

### Option 1: Double-click (Easiest)
```
1. Double-click: run_main.bat
2. Wait for generation to complete
3. Check the 'data' folder for results
```

### Option 2: Command Line
```bash
python main.py
```

## 📁 Output Structure

After running, you'll get:

```
data/
├── img1_0.png          # First image of pair 0
├── img2_0.png          # Second image of pair 0
├── img1_1.png          # First image of pair 1
├── img2_1.png          # Second image of pair 1
├── ...
├── img1_49.png
├── img2_49.png
├── dataset_metadata.json  # Complete dataset information
├── logo1.png           # Dummy logo (auto-generated)
├── logo2.png
├── logo3.png
├── inline1.png         # Dummy inline images (auto-generated)
├── inline2.png
└── inline3.png
```

## 📊 Dataset Features

### Style Attributes
Each image pair varies in these attributes:
- ✅ **Fonts** (Arial, Times, Verdana, Calibri)
- ✅ **Background colors** (4 shades of white/gray)
- ✅ **Text colors** (4 shades of black/gray)
- ✅ **Borders** (widths: 1-4 pixels)
- ✅ **Logo positions** (4 corners)
- ✅ **Bullet points** (enabled/disabled)
- ✅ **Tables** (customizable rows/columns, borders, colors)
- ✅ **Inline images** (1 or 2 images per slide)

### Dataset Balance
- **50% identical pairs**: Both images have exactly the same style
- **50% different pairs**: Images differ by one or more attributes

### Labels
Each pair has two labels:
1. **style_label**: `1` = identical, `0` = different
2. **font_label**: `1` = same font, `0` = different fonts

## ⚙️ Configuration

Edit `main.py` to customize:

### Basic Settings
```python
NUM_SAMPLES = 50        # Number of image pairs
OUTPUT_DIR = "data"     # Output folder name
img_size = (1024, 768)  # Image dimensions
```

### Table Settings
```python
TABLE_MIN_ROWS = 2      # Minimum table rows
TABLE_MAX_ROWS = 5      # Maximum table rows
TABLE_MIN_COLS = 2      # Minimum table columns
TABLE_MAX_COLS = 4      # Maximum table columns
```

### Font Paths (Important!)
Update these to match your system:
```python
font_list = [
    "C:\\Windows\\Fonts\\arial.ttf",
    "C:\\Windows\\Fonts\\times.ttf",
    "C:\\Windows\\Fonts\\verdana.ttf",
    "C:\\Windows\\Fonts\\calibri.ttf"
]
```

### Colors
```python
background_colors = ["#FFFFFF", "#F5F5F5", "#E8E8E8", "#FAFAFA"]
text_colors = ["#000000", "#1a1a1a", "#333333", "#2c2c2c"]
table_border_colors = ["#000000", "#333333", "#555555", "#777777"]
```

## 📋 Dataset Metadata

The generated `dataset_metadata.json` contains:
```json
{
  "generation_date": "2024-11-13 14:30:00",
  "num_samples": 50,
  "dataset": [
    {
      "pair_id": 0,
      "img1": "data\\img1_0.png",
      "img2": "data\\img2_0.png",
      "style_label": 1,
      "font_label": 1,
      "style_match": "identical",
      "font_match": "same"
    },
    ...
  ]
}
```

## 🎨 Image Elements

Each generated image includes:

1. **Title** (large text at top)
2. **Text content** (1-3 lines, with or without bullets)
3. **Tables** (~30% of images)
   - Customizable rows and columns
   - Headers and data cells
   - Configurable borders and colors
4. **Inline images** (~30% chance each)
   - Can have 0, 1, or 2 images per slide
   - Placed side-by-side if both present
5. **Logo** (positioned in one of 4 corners)
6. **Border** (optional, various widths)

## 🔧 Advanced Usage

### Generate 100 samples
```python
# In main.py, change:
NUM_SAMPLES = 100
```

### Large tables (5-10 rows)
```python
# In main.py, change:
TABLE_MIN_ROWS = 5
TABLE_MAX_ROWS = 10
TABLE_MIN_COLS = 3
TABLE_MAX_COLS = 6
```

### Fixed table size (exactly 4x4)
```python
# In main.py, change:
TABLE_MIN_ROWS = 4
TABLE_MAX_ROWS = 4
TABLE_MIN_COLS = 4
TABLE_MAX_COLS = 4
```

### Custom output location
```python
# In main.py, change:
OUTPUT_DIR = "my_dataset/training_data"
```

## 🖼️ Using Your Own Assets

Replace dummy assets with your own:

### Logos
Place your logos in the project directory and update:
```python
logo_path = ["my_logo1.png", "my_logo2.png", "my_logo3.png"]
```

### Inline Images
Place your images in the project directory and update:
```python
inline_img = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]
```

## 📦 Requirements

### Minimum Requirements
- **Python 3.7+**
- **Pillow 10.0.0+** (PIL for image processing)

### Installation
Install all dependencies:
```bash
pip install -r requirements.txt
```

Or install minimal requirements:
```bash
pip install Pillow
```

### Optional Dependencies (Commented in requirements.txt)
- `numpy` - For better performance with large datasets
- `pandas` - For data analysis of generated datasets  
- `matplotlib` - For visualization of dataset statistics

## 🐛 Troubleshooting

### Font not found error
- Update `font_list` in `main.py` with correct paths
- On Windows, fonts are typically in `C:\Windows\Fonts\`
- On Mac, try `/Library/Fonts/` or `/System/Library/Fonts/`
- On Linux, try `/usr/share/fonts/`

### Import error
Make sure all files are in the same directory:
- `main.py`
- `datasetGenaratorPStyle.py`

### Permission denied
- Make sure the output directory is writable
- Run as administrator if necessary

## 📊 Example Output Statistics

After generation, you'll see:
```
Dataset Statistics:
  - Total pairs generated: 50
  - Style labels: 25 identical, 25 different
  - Font labels: 28 same, 22 different
```

The dataset is automatically balanced for style labels (50/50 split).

## 🎯 Use Cases

This dataset generator is perfect for:
- Training style similarity models
- Presentation analysis
- Document comparison systems
- Visual consistency detection
- Layout recognition tasks

## 📄 License

Free to use for research and educational purposes.

---

**Happy Dataset Generating! 🎉**

