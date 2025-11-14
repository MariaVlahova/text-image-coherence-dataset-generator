# API Key Setup Guide

## Option 1: Ollama (FREE - Recommended for Testing)

**Ollama is completely FREE and runs locally on your computer. No API key needed!**

### Setup Steps:

1. **Download Ollama:**
   - Visit: https://ollama.com/download
   - Download and install for Windows

2. **Pull a model:**
   ```powershell
   ollama pull llama3.2
   ```
   For vision capabilities (if you want image analysis):
   ```powershell
   ollama pull llama3.2-vision
   ```

3. **Update your code:**
   In `main_complex2.py`, change line 32:
   ```python
   LLM_PROVIDER = "ollama"  # Changed from "openai"
   ```

4. **Run your script** - No API key needed!

---

## Option 2: OpenAI (Cheap, Cloud-based)

**Cost:** ~$0.15 per million input tokens, $0.60 per million output tokens
**Free trial:** New users get $5 free credits

### Setup Steps:

1. **Create an OpenAI account:**
   - Visit: https://platform.openai.com/signup
   - Sign up with email or Google account

2. **Get your API key:**
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (you'll only see it once!)

3. **Set the API key (choose one method):**

   **Method A: Environment Variable (Recommended)**
   ```powershell
   # In PowerShell:
   $env:OPENAI_API_KEY = "your-api-key-here"
   ```
   
   **Method B: Direct in code**
   In `main_complex2.py`, change line 33:
   ```python
   LLM_API_KEY = "your-api-key-here"  # Replace with your actual key
   ```

4. **Install OpenAI package:**
   ```powershell
   pip install openai
   ```

5. **Run your script!**

---

## Cost Comparison for 20 Images:

- **Ollama:** FREE (runs on your computer)
- **OpenAI GPT-4o-mini:** ~$0.01-0.05 (very cheap with free trial credits)
- **OpenAI GPT-4o (vision):** ~$0.10-0.30 (for image analysis)

---

## Recommendation:

**Start with Ollama** - It's free and perfect for testing. If you need better quality or don't want to install software, use OpenAI with GPT-4o-mini (very cheap).

