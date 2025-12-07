"""
LLM-based text generator for presentation slides.
Supports OpenAI API and can be extended to other providers.
Includes vision capabilities to analyze slide images.
"""

import os
import random
import json
import base64
from typing import Optional, List


class LLMTextGenerator:
    """Generate presentation slide text using LLM."""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None, enabled: bool = True):
        """
        Initialize LLM text generator.
        
        Args:
            provider: LLM provider ("openai", "ollama", "deepseek", etc.)
            api_key: API key for the provider (if None, reads from environment)
            enabled: Whether to use LLM (if False, falls back to hardcoded lists)
        """
        self.provider = provider.lower()
        self.enabled = enabled
        
        # Get API key based on provider
        if self.provider == "deepseek":
            self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        else:
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # Fallback lists if LLM is disabled or fails
        self._fallback_titles = [
            "Market Analysis Q4 2024",
            "Revenue Growth Strategy",
            "Customer Engagement Metrics",
            "Product Development Roadmap",
            "Team Performance Overview",
            "Annual Budget Forecast",
            "Digital Transformation",
            "Competitive Market Position",
            "Innovation and Research",
            "Sustainability Goals 2025",
        ]
        
        self._fallback_bullets = [
            "Increased revenue by 25% this quarter",
            "Improved customer satisfaction scores",
            "Launched three new product features",
            "Expanded market presence in Europe",
            "Reduced operational costs by 15%",
        ]
        
        self._fallback_table_headers = [
            ["Product", "Sales", "Revenue", "Growth"],
            ["Region", "Q1", "Q2", "Q3", "Q4"],
            ["Team", "Target", "Actual", "Status"],
            ["Category", "Units", "Price", "Total"],
        ]
    
    def _call_openai(self, prompt: str, max_tokens: int = 50, temperature: float = 0.8, 
                     image_path: Optional[str] = None, use_vision: bool = False) -> Optional[str]:
        """Call OpenAI API to generate text, optionally with vision."""
        try:
            import openai
            
            if not self.api_key:
                provider_name = "DEEPSEEK_API_KEY" if self.provider == "deepseek" else "OPENAI_API_KEY"
                print(f"Warning: {provider_name} not set. Falling back to hardcoded text.")
                return None
            
            # Use DeepSeek base URL if provider is deepseek
            if self.provider == "deepseek":
                client = openai.OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com/v1")
            else:
                client = openai.OpenAI(api_key=self.api_key)
            
            # Prepare messages
            messages = []
            
            if use_vision and image_path and os.path.exists(image_path):
                # Use vision model
                if self.provider == "deepseek":
                    # DeepSeek supports vision with DeepSeek-VL2 model (or DeepSeek-VL)
                    # Try DeepSeek-VL2 first, fallback to DeepSeek-VL if needed
                    model = "deepseek-vl2"
                else:
                    # Use GPT-4o for vision - most reliable and widely available
                    model = "gpt-4o"
                
                # Encode image to base64
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                
                # Determine image format
                image_format = "png" if image_path.lower().endswith('.png') else "jpeg"
                
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{image_format};base64,{image_data}"
                            }
                        }
                    ]
                })
            else:
                # Text-only model
                if self.provider == "deepseek":
                    model = "deepseek-chat"
                else:
                    model = "gpt-4o-mini"
                messages = [
                    {"role": "system", "content": "You are a professional presentation slide text generator. Generate concise, clear text suitable for business presentations."},
                    {"role": "user", "content": prompt}
                ]
            
            # Some newer models (like gpt-5-nano) require max_completion_tokens instead of max_tokens
            # and don't support custom temperature values (only default 1)
            use_max_completion_tokens = "gpt-5" in model.lower() or "o1" in model.lower()
            # Models that don't support custom temperature
            no_custom_temperature = "gpt-5" in model.lower() or "o1" in model.lower()
            
            # Prepare parameters
            params = {
                "model": model,
                "messages": messages,
            }
            
            # Add max_tokens or max_completion_tokens
            if use_max_completion_tokens:
                params["max_completion_tokens"] = max_tokens
            else:
                params["max_tokens"] = max_tokens
            
            # Add temperature only if model supports it
            if not no_custom_temperature:
                params["temperature"] = temperature
            
            try:
                response = client.chat.completions.create(**params)
                return response.choices[0].message.content.strip()
            except Exception as param_error:
                # Handle parameter errors by trying different combinations
                error_str = str(param_error)
                
                # If max_tokens fails, try max_completion_tokens
                if "max_tokens" in error_str and "max_completion_tokens" in error_str.lower():
                    try:
                        params.pop("max_tokens", None)
                        params["max_completion_tokens"] = max_tokens
                        if "temperature" in params and no_custom_temperature:
                            params.pop("temperature")
                        response = client.chat.completions.create(**params)
                        return response.choices[0].message.content.strip()
                    except:
                        pass
                
                # If temperature fails, try without it
                if "temperature" in error_str.lower():
                    try:
                        params.pop("temperature", None)
                        response = client.chat.completions.create(**params)
                        return response.choices[0].message.content.strip()
                    except:
                        pass
                
                # If max_completion_tokens fails, try max_tokens
                if "max_completion_tokens" in error_str and "max_tokens" in error_str.lower():
                    try:
                        params.pop("max_completion_tokens", None)
                        params["max_tokens"] = max_tokens
                        params.pop("temperature", None)  # Also remove temperature for safety
                        response = client.chat.completions.create(**params)
                        return response.choices[0].message.content.strip()
                    except:
                        pass
                
                # If all else fails, raise the original error
                raise param_error
        
        except ImportError:
            print("Warning: openai package not installed. Install with: pip install openai")
            return None
        except Exception as e:
            error_msg = str(e)
            error_code = None
            # Try to extract error code from the error message
            if "402" in error_msg or "insufficient" in error_msg.lower() or "balance" in error_msg.lower():
                error_code = 402
            elif "401" in error_msg or "unauthorized" in error_msg.lower():
                error_code = 401
            elif "404" in error_msg:
                error_code = 404
            
            provider_name = "DEEPSEEK_API_KEY" if self.provider == "deepseek" else "OPENAI_API_KEY"
            provider_url = "https://platform.deepseek.com" if self.provider == "deepseek" else "https://platform.openai.com"
            
            # Print detailed error for debugging
            if use_vision:
                print(f"⚠️  Vision API Error Details:")
                print(f"   Error: {error_msg}")
                print(f"   Provider: {self.provider}")
                print(f"   Model: {model if 'model' in locals() else 'unknown'}")
            
            if error_code == 402:
                print(f"\n{'='*70}")
                print(f"⚠️  ERROR: Insufficient Balance (402)")
                print(f"{'='*70}")
                print(f"Your {self.provider.upper()} API account has insufficient credits/balance.")
                print(f"\nOptions to resolve:")
                print(f"  1. Add credits to your account:")
                print(f"     → Visit: {provider_url}")
                print(f"     → Add funds to your account")
                print(f"\n  2. Switch to FREE Ollama (recommended for testing):")
                print(f"     → Install Ollama from: https://ollama.com/download")
                print(f"     → In your script, change: LLM_PROVIDER = \"ollama\"")
                print(f"     → No API key or credits needed!")
                print(f"\n  3. Switch to OpenAI (if you have credits there):")
                print(f"     → In your script, change: LLM_PROVIDER = \"openai\"")
                print(f"     → Set environment variable: $env:OPENAI_API_KEY = \"your-key\"")
                print(f"\n  4. Continue with fallback text (no LLM):")
                print(f"     → Set USE_LLM = False in your script")
                print(f"     → The script will use hardcoded text lists")
                print(f"{'='*70}\n")
            elif error_code == 401:
                print(f"  → Check your {provider_name} - API key may be invalid or expired")
                print(f"  → Visit {provider_url} to get a new API key")
            elif "404" in error_msg or "model" in error_msg.lower() or "not found" in error_msg.lower():
                if use_vision and self.provider == "deepseek":
                    print(f"  → DeepSeek vision model (deepseek-vl2 or deepseek-vl) may not be available")
                    print(f"  → Check if DeepSeek-VL models are available in your API account")
                    print(f"  → You can try: deepseek-vl2, deepseek-vl, or deepseek-chat")
                    print(f"  → Falling back to content-based text generation")
                elif use_vision and self.provider == "openai":
                    print(f"  → Vision model may not be available or accessible")
                    print(f"  → GPT-5-nano might not be available in your account")
                    print(f"  → The code will try fallback models (GPT-4o, GPT-4o-mini)")
                else:
                    print(f"  → Model may not be available. For vision, ensure you're using a vision-capable model")
            elif "rate limit" in error_msg.lower():
                print(f"  → Rate limit exceeded. Please wait and try again")
            else:
                if use_vision:
                    print(f"  → Vision API call failed. This may indicate:")
                    print(f"     - Model doesn't support vision (DeepSeek may not support vision via chat/completions)")
                    print(f"     - API endpoint issue")
                    print(f"     - Image format/encoding problem")
                else:
                    print(f"Warning: LLM API call failed: {error_msg}")
                    print(f"  → Provider: {self.provider}")
                    print(f"  → Check your {provider_name} and account status")
            
            return None
    
    def _call_ollama(self, prompt: str, model: str = "llama3.2", max_tokens: int = 50) -> Optional[str]:
        """Call Ollama API to generate text (local model)."""
        try:
            import requests
            
            url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
            
            response = requests.post(
                url,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"num_predict": max_tokens}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                print(f"Warning: Ollama API returned status {response.status_code}")
                return None
        
        except ImportError:
            print("Warning: requests package not installed. Install with: pip install requests")
            return None
        except Exception as e:
            print(f"Warning: Ollama API call failed: {e}. Falling back to hardcoded text.")
            return None
    
    def generate_title(self, context: Optional[str] = None) -> str:
        """
        Generate a presentation slide title using LLM.
        
        Args:
            context: Optional context to guide title generation
            
        Returns:
            Generated title or fallback title
        """
        if not self.enabled:
            return random.choice(self._fallback_titles)
        
        prompt = "Generate a short, professional presentation slide title (5-8 words max). "
        if context:
            prompt += f"Context: {context}. "
        prompt += "Return only the title, no quotes or extra text."
        
        if self.provider == "openai" or self.provider == "deepseek":
            result = self._call_openai(prompt, max_tokens=20)
        elif self.provider == "ollama":
            result = self._call_ollama(prompt, max_tokens=20)
        else:
            result = None
        
        if result:
            # Clean up the result (remove quotes, extra whitespace)
            result = result.strip().strip('"').strip("'")
            if len(result) > 100:  # Sanity check - titles shouldn't be too long
                result = result[:100]
            if result:
                return result
        
        # Fallback to hardcoded list
        return random.choice(self._fallback_titles)
    
    def generate_bullet_point(self, title: Optional[str] = None) -> str:
        """
        Generate a bullet point for presentations using LLM.
        
        Args:
            title: Optional slide title to make bullet point contextually relevant
            
        Returns:
            Generated bullet point or fallback bullet
        """
        if not self.enabled:
            return random.choice(self._fallback_bullets)
        
        prompt = "Generate a concise bullet point for a presentation slide (8-12 words max). "
        if title:
            prompt += f"Make it relevant to: {title}. "
        prompt += "Focus on achievements, metrics, or key points. Return only the bullet point text, no bullet symbol."
        
        if self.provider == "openai" or self.provider == "deepseek":
            result = self._call_openai(prompt, max_tokens=30)
        elif self.provider == "ollama":
            result = self._call_ollama(prompt, max_tokens=30)
        else:
            result = None
        
        if result:
            # Clean up the result
            result = result.strip().strip('"').strip("'")
            # Remove leading bullet symbols if present
            result = result.lstrip("•").lstrip("-").lstrip("*").strip()
            if len(result) > 150:  # Sanity check
                result = result[:150]
            if result:
                return result
        
        # Fallback to hardcoded list
        return random.choice(self._fallback_bullets)
    
    def generate_table_headers(self, num_cols: int, theme: Optional[str] = None) -> List[str]:
        """
        Generate table headers using LLM.
        
        Args:
            num_cols: Number of columns needed
            theme: Optional theme/context for the table
            
        Returns:
            List of header strings
        """
        if not self.enabled:
            suitable_pools = [pool for pool in self._fallback_table_headers if len(pool) >= num_cols]
            if suitable_pools:
                selected_pool = random.choice(suitable_pools)
                return selected_pool[:num_cols]
            else:
                return [f"Column {i+1}" for i in range(num_cols)]
        
        prompt = f"Generate {num_cols} professional table column headers for a presentation slide. "
        if theme:
            prompt += f"Theme: {theme}. "
        prompt += f"Return exactly {num_cols} headers, one per line, short (1-2 words each). No numbers or extra formatting."
        
        if self.provider == "openai" or self.provider == "deepseek":
            result = self._call_openai(prompt, max_tokens=50, temperature=0.7)
        elif self.provider == "ollama":
            result = self._call_ollama(prompt, max_tokens=50)
        else:
            result = None
        
        if result:
            # Parse the result - split by newlines or commas
            lines = [line.strip() for line in result.replace(",", "\n").split("\n") if line.strip()]
            # Clean up each header
            headers = []
            for line in lines:
                # Remove numbers, bullets, dashes at the start
                cleaned = line.lstrip("0123456789.-) ").strip()
                if cleaned and len(cleaned) < 30:  # Reasonable header length
                    headers.append(cleaned)
                if len(headers) >= num_cols:
                    break
            
            if len(headers) == num_cols:
                return headers[:num_cols]
        
        # Fallback to hardcoded list
        suitable_pools = [pool for pool in self._fallback_table_headers if len(pool) >= num_cols]
        if suitable_pools:
            selected_pool = random.choice(suitable_pools)
            return selected_pool[:num_cols]
        else:
            return [f"Column {i+1}" for i in range(num_cols)]
    
    def generate_table_cell_data(self, header: str, row_num: int) -> str:
        """
        Generate data for a table cell based on header type.
        
        Args:
            header: The column header
            row_num: Row number (for variety)
            
        Returns:
            Generated cell value
        """
        # For now, use the existing logic from main_img_text_coherence.py
        # This could be enhanced with LLM if needed
        header_lower = header.lower()
        
        if any(word in header_lower for word in ["sales", "revenue", "profit", "total", "price", "cost", "budget", "spent"]):
            return f"${random.randint(100, 9999):,}"
        elif any(word in header_lower for word in ["growth", "change", "margin"]):
            return f"{random.choice(['+', '-'])}{random.randint(1, 50)}%"
        elif any(word in header_lower for word in ["units", "visitors", "conversions"]):
            return str(random.randint(10, 9999))
        elif any(word in header_lower for word in ["q1", "q2", "q3", "q4", "month", "quarter"]):
            if "q" in header_lower:
                return f"Q{random.randint(1, 4)}"
            else:
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                return random.choice(months)
        elif any(word in header_lower for word in ["status", "state"]):
            return random.choice(["Active", "Pending", "Complete", "On Hold"])
        elif any(word in header_lower for word in ["region", "country"]):
            return random.choice(["USA", "UK", "Germany", "France", "Japan"])
        elif any(word in header_lower for word in ["department", "team"]):
            return random.choice(["Sales", "Marketing", "IT", "HR", "Finance"])
        elif any(word in header_lower for word in ["category", "product"]):
            return random.choice(["A", "B", "C", "D", "Premium"])
        else:
            return f"Data {row_num}"
    
    def generate_presentation_text_from_image(self, image_path: str, max_length: int = 200) -> str:
        """
        Generate presentation text by analyzing the actual slide image using vision capabilities.
        This is the text a presenter would use to explain the slide based on what's visible.
        
        Args:
            image_path: Path to the generated slide image file
            max_length: Maximum length of generated text in characters
            
        Returns:
            Generated presentation text based on image analysis
        """
        if not self.enabled:
            return f"Presentation about this slide (image analysis disabled)"
        
        if not os.path.exists(image_path):
            return f"Image not found: {image_path}"
        
        # Verify API key is available
        if (self.provider == "openai" or self.provider == "deepseek") and not self.api_key:
            provider_name = "DEEPSEEK_API_KEY" if self.provider == "deepseek" else "OPENAI_API_KEY"
            print(f"Error: {provider_name} not set. Cannot generate presentation text.")
            print(f"  → Set environment variable: $env:{provider_name} = \"your-key\"")
            return f"Presentation about this slide (API key not configured)"
        
        prompt = f"""You are analyzing a presentation slide image. Generate a short presentation script (3-5 sentences, max {max_length} characters) that a presenter would use to introduce and explain this slide to an audience.

Analyze the slide image carefully and identify:
- The title/main topic
- Key bullet points or content areas
- Any tables or data visualizations
- Overall message and purpose

The presentation text should be natural, engaging, and suitable for a business presentation. Focus on the main message and key takeaways visible in the slide. Write as if you're the presenter introducing this slide to your audience.

Return only the presentation text, no quotes or extra formatting."""

        # Try to generate presentation text using vision
        result = None
        
        # Try to generate presentation text using vision
        if self.provider == "openai" or self.provider == "deepseek":
            model_name = "DeepSeek-VL2" if self.provider == "deepseek" else "GPT-4o"
            print(f"Attempting to generate presentation text using {self.provider} vision model ({model_name})...")
            try:
                result = self._call_openai(
                    prompt, 
                    max_tokens=max_length // 4, 
                    temperature=0.8,
                    image_path=image_path,
                    use_vision=True
                )
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️  Vision API Error: {error_msg}")
                
                # If OpenAI and model not found, try GPT-4o-mini as fallback
                if self.provider == "openai" and ("404" in error_msg.lower() or "model" in error_msg.lower() or "not found" in error_msg.lower() or "does not exist" in error_msg.lower()):
                    print(f"  GPT-4o may not be available. Trying GPT-4o-mini as fallback...")
                    try:
                        import openai
                        if not self.api_key:
                            result = None
                        else:
                            client = openai.OpenAI(api_key=self.api_key)
                            with open(image_path, "rb") as image_file:
                                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                            image_format = "png" if image_path.lower().endswith('.png') else "jpeg"
                            
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[{
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": prompt},
                                        {
                                            "type": "image_url",
                                            "image_url": {"url": f"data:image/{image_format};base64,{image_data}"}
                                        }
                                    ]
                                }],
                                max_tokens=max_length // 4,
                                temperature=0.8,
                            )
                            result = response.choices[0].message.content.strip()
                            print(f"  ✓ Successfully used GPT-4o-mini model for vision")
                    except Exception as e2:
                        print(f"  GPT-4o-mini also failed: {e2}")
                        result = None
                # If DeepSeek-VL2 fails, try DeepSeek-VL as fallback
                elif self.provider == "deepseek" and ("404" in error_msg.lower() or "model" in error_msg.lower() or "not found" in error_msg.lower()):
                    print(f"  DeepSeek-VL2 not available, trying DeepSeek-VL...")
                    try:
                        import openai
                        if not self.api_key:
                            result = None
                        else:
                            client = openai.OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com/v1")
                            with open(image_path, "rb") as image_file:
                                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                            image_format = "png" if image_path.lower().endswith('.png') else "jpeg"
                            
                            response = client.chat.completions.create(
                                model="deepseek-vl",
                                messages=[{
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": prompt},
                                        {
                                            "type": "image_url",
                                            "image_url": {"url": f"data:image/{image_format};base64,{image_data}"}
                                        }
                                    ]
                                }],
                                max_tokens=max_length // 4,
                                temperature=0.8,
                            )
                            result = response.choices[0].message.content.strip()
                            print(f"  ✓ Successfully used DeepSeek-VL model")
                    except Exception as e2:
                        print(f"  DeepSeek-VL also failed: {e2}")
                        result = None
                else:
                    print(f"  Vision API call failed. Error details: {error_msg}")
                    result = None
        elif self.provider == "ollama":
            # For Ollama, try to use vision model if available
            print(f"Attempting to generate presentation text using Ollama vision model...")
            result = self._call_ollama_vision(prompt, image_path, max_tokens=max_length // 4)
        else:
            print(f"Warning: Unknown provider '{self.provider}' for vision generation")
            result = None
        
        if result:
            # Clean up the result
            result = result.strip().strip('"').strip("'")
            # Limit to max_length
            if len(result) > max_length:
                # Try to cut at sentence boundary
                sentences = result.split('. ')
                result = sentences[0]
                if len(result) < max_length * 0.7 and len(sentences) > 1:
                    result = '. '.join(sentences[:2])
                if len(result) > max_length:
                    result = result[:max_length - 3] + "..."
            
            if result and len(result.strip()) > 10:  # Ensure we have meaningful content
                print(f"Successfully generated presentation text ({len(result)} chars)")
                return result
            else:
                print(f"Warning: Generated text too short or empty, retrying...")
        
        # If vision failed, try generating text without vision as fallback
        if result is None:
            print(f"Vision analysis failed, attempting text-only generation based on image path...")
            
            # Check if API key is available before trying fallback
            if (self.provider == "openai" or self.provider == "deepseek") and not self.api_key:
                provider_name = "DEEPSEEK_API_KEY" if self.provider == "deepseek" else "OPENAI_API_KEY"
                print(f"  ✗ Error: {provider_name} not set. Cannot generate presentation text.")
                print(f"  → Set environment variable: $env:{provider_name} = \"your-key\"")
                return f"Presentation about this slide (API key not configured)"
            
            fallback_prompt = f"""Generate a short presentation script (3-5 sentences, max {max_length} characters) for a presentation slide. 
The slide likely contains business content such as titles, bullet points, tables, and data visualizations.
Write as if you're a presenter introducing this slide to an audience. Be natural and engaging.
Return only the presentation text, no quotes or extra formatting."""
            
            try:
                if self.provider == "openai" or self.provider == "deepseek":
                    result = self._call_openai(fallback_prompt, max_tokens=max_length // 4, temperature=0.8)
                elif self.provider == "ollama":
                    result = self._call_ollama(fallback_prompt, max_tokens=max_length // 4)
            except Exception as fallback_error:
                print(f"  ✗ Fallback text generation also failed: {fallback_error}")
                result = None
        
        if result:
            result = result.strip().strip('"').strip("'")
            if len(result) > max_length:
                result = result[:max_length - 3] + "..."
            if result and len(result.strip()) > 10:
                print(f"Generated presentation text using fallback method ({len(result)} chars)")
                return result
        
        # Last resort fallback - provide detailed error information
        print(f"\n✗ Error: Could not generate presentation text.")
        print(f"  Provider: {self.provider}")
        if self.provider == "openai" or self.provider == "deepseek":
            provider_name = "DEEPSEEK_API_KEY" if self.provider == "deepseek" else "OPENAI_API_KEY"
            api_key_set = "✓ Set" if self.api_key else "✗ Not set"
            print(f"  API Key: {api_key_set}")
            if not self.api_key:
                print(f"  → Set environment variable: $env:{provider_name} = \"your-key\"")
            else:
                print(f"  → Check if your API key is valid and has sufficient credits")
                print(f"  → Verify the model (GPT-5-nano) is available in your account")
        return f"Presentation about this slide (analysis unavailable)"
    
    def _call_ollama_vision(self, prompt: str, image_path: str, model: str = "llama3.2-vision", max_tokens: int = 50) -> Optional[str]:
        """Call Ollama API with vision support (if available)."""
        try:
            import requests
            
            url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
            
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Check if vision model is available, fallback to regular model
            full_prompt = f"{prompt}\n\n[Image data attached]"
            
            response = requests.post(
                url,
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "images": [image_data],
                    "stream": False,
                    "options": {"num_predict": max_tokens}
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                # Fallback to regular model
                print(f"Warning: Ollama vision model not available, trying text-only")
                return self._call_ollama(prompt, max_tokens=max_tokens)
        
        except ImportError:
            print("Warning: requests package not installed. Install with: pip install requests")
            return None
        except Exception as e:
            print(f"Warning: Ollama vision API call failed: {e}. Trying text-only fallback.")
            return self._call_ollama(prompt, max_tokens=max_tokens)
    
    def generate_presentation_text_from_content(self, title: str, bullet_points: List[str], 
                                                 table_headers: Optional[List[str]] = None, 
                                                 max_length: int = 200) -> str:
        """
        Generate presentation text based on slide content (title, bullets, table headers).
        This is a fallback when vision analysis is not available.
        
        Args:
            title: Slide title
            bullet_points: List of bullet points
            table_headers: Optional list of table headers
            max_length: Maximum length of generated text in characters
            
        Returns:
            Generated presentation text
        """
        if not self.enabled:
            return f"Presentation about this slide (LLM disabled)"
        
        bullets_text = "\n".join([f"- {bp}" for bp in bullet_points])
        table_info = f"\nTable Headers: {', '.join(table_headers)}" if table_headers else ""
        
        prompt = f"""Generate a short presentation script (3-5 sentences, max {max_length} characters) for a presentation slide with the following content:

Title: {title}
Key Points:
{bullets_text}{table_info}

Write as if you're a presenter introducing this slide to an audience. Be natural, engaging, and focus on the main message. Return only the presentation text, no quotes or extra formatting."""
        
        if self.provider == "openai" or self.provider == "deepseek":
            result = self._call_openai(prompt, max_tokens=max_length // 4, temperature=0.8)
        elif self.provider == "ollama":
            result = self._call_ollama(prompt, max_tokens=max_length // 4)
        else:
            result = None
        
        if result:
            result = result.strip().strip('"').strip("'")
            if len(result) > max_length:
                result = result[:max_length - 3] + "..."
            if result and len(result.strip()) > 20:
                return result
        
        # Fallback: create simple description
        bullets_desc = " and ".join([bp.lower() for bp in bullet_points[:2]])
        table_desc = f" with a data table showing {', '.join(table_headers[:3])}" if table_headers else ""
        return f"This slide presents {title.lower()}. Key highlights include {bullets_desc}.{table_desc}."

