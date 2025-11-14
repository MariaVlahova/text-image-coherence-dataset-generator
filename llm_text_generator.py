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
            provider: LLM provider ("openai", "ollama", etc.)
            api_key: API key for the provider (if None, reads from environment)
            enabled: Whether to use LLM (if False, falls back to hardcoded lists)
        """
        self.provider = provider.lower()
        self.enabled = enabled
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
                print("Warning: OPENAI_API_KEY not set. Falling back to hardcoded text.")
                return None
            
            client = openai.OpenAI(api_key=self.api_key)
            
            # Prepare messages
            messages = []
            
            if use_vision and image_path and os.path.exists(image_path):
                # Use vision model (GPT-4 Vision)
                model = "gpt-4o"  # or "gpt-4o-mini" for cost-effective option
                
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
                model = "gpt-4o-mini"
                messages = [
                    {"role": "system", "content": "You are a professional presentation slide text generator. Generate concise, clear text suitable for business presentations."},
                    {"role": "user", "content": prompt}
                ]
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            return response.choices[0].message.content.strip()
        
        except ImportError:
            print("Warning: openai package not installed. Install with: pip install openai")
            return None
        except Exception as e:
            print(f"Warning: LLM API call failed: {e}. Falling back to hardcoded text.")
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
        
        if self.provider == "openai":
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
        
        if self.provider == "openai":
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
        
        if self.provider == "openai":
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
        
        prompt = f"""You are analyzing a presentation slide image. Generate a short presentation script (2-3 sentences, max {max_length} characters) that a presenter would use to introduce and explain this slide to an audience.

Analyze the slide image carefully and identify:
- The title/main topic
- Key bullet points or content areas
- Any tables or data visualizations
- Overall message and purpose

The presentation text should be natural, engaging, and suitable for a business presentation. Focus on the main message and key takeaways visible in the slide. Write as if you're the presenter introducing this slide to your audience.

Return only the presentation text, no quotes or extra formatting."""

        if self.provider == "openai":
            result = self._call_openai(
                prompt, 
                max_tokens=max_length // 4, 
                temperature=0.8,
                image_path=image_path,
                use_vision=True
            )
        elif self.provider == "ollama":
            # For Ollama, try to use vision model if available
            result = self._call_ollama_vision(prompt, image_path, max_tokens=max_length // 4)
        else:
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
            return result
        
        # Fallback
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

