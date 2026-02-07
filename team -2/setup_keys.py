"""
Setup script for API keys
Run this to set up environment variables for better search results
"""

import os
import sys

def setup_api_keys():
    """Interactive setup for API keys"""
    
    print("🔑 Web Search Module - API Key Setup")
    print("=" * 50)
    print("This script will help you set up API keys for better search results.")
    print("You can skip this if you want to use the free scraping method.")
    print()
    
    # Get SerpAPI key
    serpapi_key = input("Enter SerpAPI key (or press Enter to skip): ").strip()
    if serpapi_key:
        os.environ['SERPAPI_KEY'] = serpapi_key
        print("✅ SerpAPI key set")
    
    # Get Bing API key
    bing_key = input("Enter Bing API key (or press Enter to skip): ").strip()
    if bing_key:
        os.environ['BING_API_KEY'] = bing_key
        print("✅ Bing API key set")
    
    if not serpapi_key and not bing_key:
        print("\n📝 No API keys set. The module will use free web scraping.")
        print("This works well with DuckDuckGo and other search engines.")
    else:
        print("\n🚀 API keys configured! You'll get better search results.")
    
    print("\n💡 To make these changes permanent:")
    print("Windows: setx SERPAPI_KEY \"your_key\"")
    print("Linux/Mac: export SERPAPI_KEY=\"your_key\"")
    
    return serpapi_key, bing_key

if __name__ == "__main__":
    setup_api_keys()
