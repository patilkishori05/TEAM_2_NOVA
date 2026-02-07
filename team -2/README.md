# Team Member 3 - Web Search Module

## Overview
This module provides asynchronous web search functionality with multiple fallback options for finding relevant URLs and titles based on search queries.

## Features
- **Multiple Search Methods**: SerpAPI → Bing API → Google Scraping
- **Async Processing**: Concurrent search of multiple queries
- **Duplicate Removal**: Automatic deduplication of results
- **Error Handling**: Graceful fallbacks between methods
- **Team 4 Integration**: Returns data in expected JSON format

## Files
- `web_search.py` - Main search module
- `test_search.py` - Demo and testing script
- `requirements.txt` - Python dependencies

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```python
import asyncio
from web_search import search_multiple_queries

async def main():
    queries = ["AI in healthcare", "machine learning in hospitals"]
    results = await search_multiple_queries(queries)
    print(results)

asyncio.run(main())
```

### Expected Output Format
```json
[
  {
    "url": "https://example.com/ai-healthcare",
    "title": "AI in Medicine: Transforming Healthcare"
  },
  {
    "url": "https://example.com/ml-hospitals", 
    "title": "Machine Learning Applications in Hospitals"
  }
]
```

## API Keys (Optional)
Set environment variables for better search results:
- `SERPAPI_KEY` - For SerpAPI integration
- `BING_API_KEY` - For Bing Web Search API

If no API keys are provided, the module falls back to Google scraping.

## Testing
```bash
python test_search.py
```

## Main Function
```python
async def search_multiple_queries(queries: list[str]) -> list[dict]:
    """Search multiple queries and return combined results"""
```

## Architecture
1. **SerpAPI** (Primary) - Professional search API
2. **Bing API** (Secondary) - Microsoft search API  
3. **Google Scraping** (Fallback) - Direct web scraping with BeautifulSoup

All methods run concurrently for maximum performance.
