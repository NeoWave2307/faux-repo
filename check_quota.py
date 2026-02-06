"""
Quick quota and API health check script.
Run this to check if your API key is working and has available quota.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def check_quota():
    """Check API quota status with a minimal request."""
    print("=" * 60)
    print("🔍 Gemini API Quota Check")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ API key not configured in .env file")
        print("   Get your key: https://makersuite.google.com/app/apikey")
        return False
    
    print(f"✅ API key loaded: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        print("\n🧪 Testing API with minimal request...")
        
        # Use the fastest model for quota check
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",  # Fastest model
            contents="Reply with just the word 'OK'"
        )
        
        print("✅ API is working!")
        print(f"   Response: {response.text.strip()}")
        print("\n✅ Your quota is available. You can use the app now!")
        print("\n💡 Free tier limits:")
        print("   - 15 requests per minute")
        print("   - 1,500 requests per day")
        print("   - Check your usage: https://aistudio.google.com/apikey")
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"\n❌ API Error: {error_str[:200]}")
        
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            print("\n⚠️  QUOTA EXCEEDED")
            print("   You've used up your free tier quota.")
            print("\n   What to do:")
            print("   1. Wait a few minutes (rate limit resets)")
            print("   2. Check if you hit daily limit (1500 requests/day)")
            print("   3. Monitor usage: https://aistudio.google.com/apikey")
            print("   4. Consider getting a new API key if daily limit hit")
        elif "401" in error_str or "UNAUTHORIZED" in error_str:
            print("\n⚠️  INVALID API KEY")
            print("   Your API key is not valid or has been revoked.")
            print("   Get a new key: https://makersuite.google.com/app/apikey")
        elif "404" in error_str:
            print("\n⚠️  MODEL NOT FOUND")
            print("   The model name might have changed.")
            print("   Run: python test_gemini_api.py to find available models")
        else:
            print("\n⚠️  UNKNOWN ERROR")
            print("   Check your internet connection and API key status")
        
        return False
    
    print("=" * 60)

if __name__ == "__main__":
    success = check_quota()
    exit(0 if success else 1)
