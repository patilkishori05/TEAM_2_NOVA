import asyncio
import json
from web_search import search_multiple_queries

async def demo_search():
    """Demo the web search functionality with sample queries"""
    
    # Sample queries for testing
    queries = [
        "AI in healthcare",
        "machine learning in hospitals"
    ]
    
    print("🔍 Web Search Module Demo")
    print("=" * 50)
    print(f"Searching for: {queries}")
    print()
    
    try:
        results = await search_multiple_queries(queries)
        
        print(f"Found {len(results)} results:")
        print("-" * 50)
        
        for i, result in enumerate(results[:10], 1):
            print(f"{i}. {result['title']}")
            print(f"   🔗 {result['url']}")
            print()
        
        # Show the output format for Team 4
        print("📤 Output format for Team 4:")
        print("-" * 30)
        print(json.dumps(results[:5], indent=2))
        
        return results
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return []

async def mock_search_demo():
    """Demo with mock results when APIs are not available"""
    
    print("🎭 Mock Search Demo (No API Keys)")
    print("=" * 50)
    
    # Mock results to demonstrate the expected output format
    mock_results = [
        {
            "url": "https://example.com/ai-healthcare",
            "title": "AI in Medicine: Transforming Healthcare"
        },
        {
            "url": "https://example.com/ml-hospitals", 
            "title": "Machine Learning Applications in Hospitals"
        },
        {
            "url": "https://example.com/ai-diagnosis",
            "title": "AI-Powered Medical Diagnosis Systems"
        },
        {
            "url": "https://example.com/healthcare-automation",
            "title": "Automation in Healthcare with AI"
        },
        {
            "url": "https://example.com/predictive-medicine",
            "title": "Predictive Analytics in Medicine"
        }
    ]
    
    print("Sample output for Team 4:")
    print("-" * 30)
    print(json.dumps(mock_results, indent=2))
    
    return mock_results

if __name__ == "__main__":
    print("🚀 Team Member 3 - Web Search Module")
    print("=" * 50)
    
    # Try real search first
    try:
        asyncio.run(demo_search())
    except Exception as e:
        print(f"Real search failed: {e}")
        print("Running mock demo...")
        asyncio.run(mock_search_demo())
