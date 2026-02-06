"""
Google Gemini client for curriculum generation.
Uses free tier: 15 requests/min, 1500 requests/day.
"""
import os
from typing import Optional
from google import genai
from dotenv import load_dotenv


class GeminiClient:
    """Google Gemini LLM client wrapper."""
    
    def __init__(self, model_name: str = "models/gemini-2.5-flash"):
        """
        Initialize Gemini client.
        
        Args:
            model_name: Gemini model to use (default: models/gemini-2.5-flash)
        """
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found in environment variables. "
                "Please create a .env file with your API key. "
                "Get your key from: https://aistudio.google.com/apikey"
            )
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        
        print(f"OK Gemini client initialized: {model_name}")
        print(f"  Free tier: 15 requests/min, 1500 requests/day")
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using Gemini.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens if max_tokens else 8192
                }
            )
            return response.text
        
        except Exception as e:
            # Print detailed error for debugging
            error_str = str(e)
            print(f"ERROR Gemini API Error: {type(e).__name__}")
            print(f"   Error details: {error_str}")
            
            # Provide helpful messages for common errors
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print("\n⚠️  QUOTA EXCEEDED: You've hit your API rate limit.")
                print("   Free tier limits: 15 requests/min, 1500 requests/day")
                print("   Wait a few minutes and try again.")
                print("   Check quota: https://aistudio.google.com/apikey")
            elif "404" in error_str or "not found" in error_str.lower():
                print(f"\n⚠️  MODEL NOT FOUND: {self.model_name}")
                print("   Try using: models/gemini-2.5-flash or models/gemini-2.5-pro")
            
            raise Exception(f"Gemini generation failed: {error_str}")
    
    def generate_with_retry(
        self,
        prompt: str,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """
        Generate with automatic retry on failure.
        
        Args:
            prompt: Input prompt
            max_retries: Maximum retry attempts
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text
        """
        import time
        
        for attempt in range(max_retries):
            try:
                return self.generate(prompt, **kwargs)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"WARNING Attempt {attempt + 1} failed: {str(e)[:100]}")
                    print(f"  Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"ERROR All {max_retries} attempts failed!")
                    print(f"   Final error: {str(e)}")
                    raise e
