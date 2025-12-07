# Presentation Style Dataset Generator

Generate complex presentation slide images with LLM-generated text for machine learning applications. This tool creates presentation-style images with tables, logos, inline images, bullets, and borders, all with AI-generated meaningful content.

## 📦 Installation

### Prerequisites
- **Python 3.7+**
- **Windows** (fonts configured for Windows paths)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install minimal requirements:
```bash
pip install Pillow pandas openai
```

**Note:** If you're using Ollama (free local option), you only need `Pillow` and `pandas`. The `openai` package is only needed for OpenAI/DeepSeek providers.

## 🔑 LLM API Key Setup

This project uses LLMs to generate meaningful text content. You have three options:

### Option 1: Ollama (FREE - Recommended for Testing)

**Ollama runs locally on your computer - no API key needed!**

1. **Download and install Ollama:**
   - Visit: https://ollama.com/download
   - Download and install for Windows

2. **Pull a model:**
   ```powershell
   ollama pull llama3.2
   ```
   
   For vision capabilities (image analysis):
   ```powershell
   ollama pull llama3.2-vision
   ```

3. **Configure the script:**
   In `main_img_text_coherence.py`, set:
   ```python
   LLM_PROVIDER = "ollama"
   LLM_API_KEY = None  # No API key needed
   ```

### Option 2: OpenAI (Cloud-based, Paid)

**Cost:** ~$0.15 per million input tokens, $0.60 per million output tokens  
**Free trial:** New users get $5 free credits

1. **Get your API key:**
   - Visit: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (you'll only see it once!)

2. **Set the API key (choose one method):**

   **Method A: Environment Variable (Recommended)**
   ```powershell
   # In PowerShell:
   $env:OPENAI_API_KEY = "sk-your-api-key-here"
   ```
   
   **Method B: Direct in code**
   In `main_img_text_coherence.py`, change line 35:
   ```python
   LLM_API_KEY = "sk-your-api-key-here"  # Replace with your actual key
   ```

3. **Configure the script:**
   ```python
   LLM_PROVIDER = "openai"
   ```

### Option 3: DeepSeek (Cost-effective Alternative)

1. **Get your API key:**
   - Visit: https://platform.deepseek.com
   - Sign up and get your API key

2. **Set the API key:**

   **Method A: Environment Variable (Recommended)**
   ```powershell
   # In PowerShell:
   $env:DEEPSEEK_API_KEY = "your-api-key-here"
   ```
   
   **Method B: Direct in code**
   In `main_img_text_coherence.py`, change line 35:
   ```python
   LLM_API_KEY = "your-api-key-here"
   ```

3. **Configure the script:**
   ```python
   LLM_PROVIDER = "deepseek"
   ```

## 🚀 Running the Project

### Quick Start

1. **Configure your LLM provider** (see above)

2. **Run the script:**
   ```bash
   python main_img_text_coherence.py
   ```

3. **Check the output:**
   - Generated images: `generated_data/` folder
   - Metadata: `generated_data/dataset_metadata.json`
   - Presentation texts: `generated_data/presentation_texts.txt`
   - Results CSV: `result.csv`

### Example: Running with OpenAI API Key

```powershell
# Set API key in PowerShell
$env:OPENAI_API_KEY = "sk-your-key-here"

# Run the script
python main_img_text_coherence.py
```

### Example: Running with DeepSeek API Key

```powershell
# Set API key in PowerShell
$env:DEEPSEEK_API_KEY = "your-key-here"

# Run the script
python main_img_text_coherence.py
```

### Example: Running with Ollama (No API Key)

```powershell
# Make sure Ollama is running (it should start automatically)
# Then just run:
python main_img_text_coherence.py
```

## ⚙️ Configuration

Edit `main_img_text_coherence.py` to customize settings:

### Basic Settings
```python
NUM_SAMPLES = 20                    # Number of images to generate
OUTPUT_DIR = "generated_data"       # Output folder name
img_size = (224, 224)               # Image dimensions (width x height)
```

### LLM Settings
```python
USE_LLM = True                       # Set to False to use hardcoded text
LLM_PROVIDER = "deepseek"            # Options: "openai", "ollama", "deepseek"
LLM_API_KEY = None                  # Set here or use environment variable
GENERATE_PRESENTATION_TEXT = True   # Generate text by analyzing images (requires vision model)
PRESENTATION_TEXT_MAX_LENGTH = 200  # Maximum length of presentation text
```

### Table Settings
```python
TABLE_MIN_ROWS = 2
TABLE_MAX_ROWS = 4
TABLE_MIN_COLS = 2
TABLE_MAX_COLS = 4
```

### Font Paths (Windows)
The default fonts are configured for Windows. If you're on a different system, update:
```python
font_list = [
    "C:\\Windows\\Fonts\\arial.ttf",
    "C:\\Windows\\Fonts\\arialbd.ttf",
    "C:\\Windows\\Fonts\\times.ttf",
    # ... add more fonts
]
```

## 📁 Output Structure

After running, you'll get:

```
generated_data/
├── img1_0.png              # Generated image 0
├── img1_1.png              # Generated image 1
├── ...
├── img1_19.png             # Generated image 19
├── dataset_metadata.json   # Complete dataset information
└── presentation_texts.txt # Generated presentation texts

result.csv                  # Results in CSV format
```

### Dataset Metadata Example
```json
{
  "generation_date": "2024-11-13 14:30:00",
  "num_samples": 20,
  "complex_images": true,
  "all_features_enabled": true,
  "presentation_texts_enabled": true,
  "dataset": [
    {
      "image_id": 0,
      "image_path": "generated_data\\img1_0.png",
      "presentation_text": "This slide presents quarterly sales data...",
      "filename": "img1_0.png"
    }
  ]
}
```

## 📊 Dataset Features

### Complex Images (All Features Enabled)
Each generated image includes:
- ✅ **Title** (LLM-generated, max 2 rows)
- ✅ **Bullet points** (2 bullet points, LLM-generated)
- ✅ **Tables** (2-4 rows, 2-4 columns, LLM-generated headers and data)
- ✅ **Logos** (positioned in one of 4 corners)
- ✅ **Inline images** (always 2 images per slide)
- ✅ **Borders** (2-5 pixels width)
- ✅ **Presentation text** (generated by analyzing the image with vision model)

### Style Attributes
- **Fonts**: Arial, Times, Verdana, Calibri, Georgia (with bold variants)
- **Background colors**: 10 shades of white/gray
- **Text colors**: 10 shades of black/gray
- **Table borders**: Various widths and colors
- **Logo positions**: 4 corners (top-left, top-right, bottom-left, bottom-right)

## 🔧 Advanced Usage

### Disable LLM (Use Hardcoded Text)
```python
USE_LLM = False  # Will use fallback text lists
```

### Disable Presentation Text Generation
```python
GENERATE_PRESENTATION_TEXT = False  # Skips image analysis
```

### Generate More Samples
```python
NUM_SAMPLES = 100  # Generate 100 images
```

### Custom Output Directory
```python
OUTPUT_DIR = "my_custom_dataset"
```

## 🖼️ Using Your Own Assets

### Logos
Place your logos in the `data/` folder and update:
```python
logo_path = ["data/my_logo1.png", "data/my_logo2.png", ...]
```

### Inline Images
Place your images in the `data/` folder and update:
```python
inline_img = ["data/pres2.png", "data/pres3.png", ...]
```

**Note:** If assets don't exist, the script will auto-generate dummy placeholders.

## 🐛 Troubleshooting

### "API key not set" Warning
- **For OpenAI:** Set `OPENAI_API_KEY` environment variable or `LLM_API_KEY` in code
- **For DeepSeek:** Set `DEEPSEEK_API_KEY` environment variable or `LLM_API_KEY` in code
- **For Ollama:** Make sure Ollama is installed and running (no API key needed)

### Font Not Found Error
- Update `font_list` in `main_img_text_coherence.py` with correct paths
- On Windows: fonts are in `C:\Windows\Fonts\`
- On Mac: try `/Library/Fonts/` or `/System/Library/Fonts/`
- On Linux: try `/usr/share/fonts/`

### Ollama Connection Error
- Make sure Ollama is installed and running
- Check if Ollama service is running: `ollama list` (should show your models)
- Default URL is `http://localhost:11434`

### Import Error
Make sure all required files are in the same directory:
- `main_img_text_coherence.py`
- `llm_text_generator.py`

### Permission Denied
- Make sure the output directory is writable
- Run as administrator if necessary

## 💰 Cost Estimates

For generating 20 images:
- **Ollama:** FREE (runs locally)
- **OpenAI GPT-4o-mini:** ~$0.01-0.05 (very cheap)
- **OpenAI GPT-4o (with vision):** ~$0.10-0.30 (for image analysis)
- **DeepSeek:** Similar to OpenAI, often cheaper

## 📋 Requirements

### Required
- `Pillow>=10.0.0` - Image processing
- `pandas` - Data handling

### Optional (for LLM)
- `openai>=1.0.0` - For OpenAI/DeepSeek providers
- `requests>=2.31.0` - For Ollama (usually pre-installed)

## 🎯 Use Cases

This dataset generator is perfect for:
- Training image-text coherence models
- Presentation style analysis
- Document understanding systems
- Visual consistency detection
- Layout recognition tasks
- Multi-modal learning research

## 📄 Additional Resources

- See `API_KEY_SETUP.md` for detailed API key setup instructions
- Check `generated_data/dataset_metadata.json` for complete dataset information

## 📄 License

Free to use for research and educational purposes.

---

**Happy Dataset Generating! 🎉**
