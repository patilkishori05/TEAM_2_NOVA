import asyncio
import aiohttp
import os
import json
from typing import List, Dict, Optional
from urllib.parse import quote_plus
import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSearchModule:
    def __init__(self):
        self.serpapi_key = os.getenv('SERPAPI_KEY')
        self.bing_api_key = os.getenv('BING_API_KEY')
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    async def search_with_serpapi(self, query: str, session: aiohttp.ClientSession) -> List[Dict[str, str]]:
        """Search using SerpAPI"""
        if not self.serpapi_key:
            logger.warning("SerpAPI key not found")
            return []
        
        url = "https://serpapi.com/search"
        params = {
            'api_key': self.serpapi_key,
            'engine': 'google',
            'q': query,
            'num': 10  # Number of results
        }
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    if 'organic_results' in data:
                        for result in data['organic_results'][:10]:
                            results.append({
                                'url': result.get('link', ''),
                                'title': result.get('title', '')
                            })
                    
                    logger.info(f"SerpAPI found {len(results)} results for: {query}")
                    return results
                else:
                    logger.error(f"SerpAPI error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"SerpAPI exception: {str(e)}")
            return []
    
    async def search_with_bing(self, query: str, session: aiohttp.ClientSession) -> List[Dict[str, str]]:
        """Search using Bing Web Search API"""
        if not self.bing_api_key:
            logger.warning("Bing API key not found")
            return []
        
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {
            'Ocp-Apim-Subscription-Key': self.bing_api_key
        }
        params = {
            'q': query,
            'count': 10,
            'mkt': 'en-US'
        }
        
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    if 'webPages' in data and 'value' in data['webPages']:
                        for result in data['webPages']['value']:
                            results.append({
                                'url': result.get('url', ''),
                                'title': result.get('name', '')
                            })
                    
                    logger.info(f"Bing API found {len(results)} results for: {query}")
                    return results
                else:
                    logger.error(f"Bing API error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Bing API exception: {str(e)}")
            return []
    
    async def search_with_scraping(self, query: str, session: aiohttp.ClientSession) -> List[Dict[str, str]]:
        """Search using multiple sources with BeautifulSoup (fallback method)"""
        
        # Try multiple search engines
        search_engines = [
            {
                'name': 'DuckDuckGo',
                'url': f"https://duckduckgo.com/html/?q={quote_plus(query)}",
                'parser': self._parse_duckduckgo
            },
            {
                'name': 'Brave Search', 
                'url': f"https://search.brave.com/search?q={quote_plus(query)}",
                'parser': self._parse_brave
            },
            {
                'name': 'Google',
                'url': f"https://www.google.com/search?q={quote_plus(query)}&num=10",
                'parser': self._parse_google
            }
        ]
        
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        for engine in search_engines:
            try:
                async with session.get(engine['url'], headers=headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        results = engine['parser'](html)
                        
                        if results:
                            logger.info(f"{engine['name']} found {len(results)} results for: {query}")
                            return results
                    else:
                        logger.warning(f"{engine['name']} returned status: {response.status}")
                        
            except Exception as e:
                logger.warning(f"{engine['name']} failed: {str(e)}")
                continue
        
        logger.error(f"All search engines failed for: {query}")
        return []
    
    def _parse_duckduckgo(self, html: str) -> List[Dict[str, str]]:
        """Parse DuckDuckGo search results"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            # DuckDuckGo uses specific classes for results
            search_results = soup.find_all('div', class_='result')
            
            for result in search_results[:10]:
                link_elem = result.find('a', class_='result__a')
                title_elem = result.find('a', class_='result__a')
                
                if link_elem and title_elem:
                    url = link_elem.get('href', '')
                    title = title_elem.get_text(strip=True)
                    
                    if url.startswith('http') and title and len(title) > 3:
                        results.append({
                            'url': url,
                            'title': title
                        })
            
            return results
        except Exception as e:
            logger.error(f"DuckDuckGo parsing error: {str(e)}")
            return []
    
    def _parse_brave(self, html: str) -> List[Dict[str, str]]:
        """Parse Brave search results"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            # Brave uses different structure
            search_results = soup.find_all('div', {'data-type': 'web'})
            
            for result in search_results[:10]:
                link_elem = result.find('a')
                title_elem = result.find('h3')
                
                if link_elem and title_elem:
                    url = link_elem.get('href', '')
                    title = title_elem.get_text(strip=True)
                    
                    if url.startswith('http') and title and len(title) > 3:
                        results.append({
                            'url': url,
                            'title': title
                        })
            
            # Fallback: look for any links with titles
            if not results:
                all_links = soup.find_all('a', href=True)
                for link in all_links[:15]:
                    href = link.get('href', '')
                    if (href.startswith('http') and 
                        'brave.com' not in href and 
                        len(href) > 10):
                        title = link.get_text(strip=True)
                        if title and len(title) > 5 and len(title) < 100:
                            results.append({
                                'url': href,
                                'title': title
                            })
                            if len(results) >= 10:
                                break
            
            return results
        except Exception as e:
            logger.error(f"Brave parsing error: {str(e)}")
            return []
    
    def _parse_google(self, html: str) -> List[Dict[str, str]]:
        """Parse Google search results"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            # Try multiple Google result selectors
            selectors = [
                'div.g',
                'div[data-ved]', 
                'div.tF2Cxc',
                'div.yuRUbf'
            ]
            
            for selector in selectors:
                search_results = soup.find_all('div', class_=selector.split('.')[-1] if '.' in selector else selector)
                
                for result in search_results[:10]:
                    link_elem = result.find('a')
                    title_elem = result.find('h3') or result.find('h2')
                    
                    if link_elem and title_elem:
                        url = link_elem.get('href', '')
                        title = title_elem.get_text(strip=True)
                        
                        # Clean Google URLs
                        if url.startswith('/url?q='):
                            url = url.split('/url?q=')[1].split('&')[0]
                        
                        if (url.startswith('http') and 
                            'google.com' not in url and 
                            title and 
                            len(title) > 3):
                            results.append({
                                'url': url,
                                'title': title
                            })
                
                if results:
                    break
            
            return results
        except Exception as e:
            logger.error(f"Google parsing error: {str(e)}")
            return []
    
    async def search_single_query(self, query: str) -> List[Dict[str, str]]:
        """Search a single query using available methods in order of preference"""
        async with aiohttp.ClientSession() as session:
            # Try SerpAPI first
            if self.serpapi_key:
                results = await self.search_with_serpapi(query, session)
                if results:
                    return results
            
            # Try Bing API second
            if self.bing_api_key:
                results = await self.search_with_bing(query, session)
                if results:
                    return results
            
            # Fall back to scraping
            results = await self.search_with_scraping(query, session)
            return results

async def search_multiple_queries(queries: List[str]) -> List[Dict[str, str]]:
    """
    Search multiple queries and return combined results
    
    Args:
        queries: List of search queries
        
    Returns:
        List of dictionaries with 'url' and 'title' keys
    """
    searcher = WebSearchModule()
    all_results = []
    
    # Create tasks for concurrent searching
    tasks = [searcher.search_single_query(query) for query in queries]
    
    # Execute all searches concurrently
    results_lists = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Combine all results
    for i, results in enumerate(results_lists):
        if isinstance(results, Exception):
            logger.error(f"Error searching query '{queries[i]}': {str(results)}")
            continue
        
        all_results.extend(results)
    
    # Remove duplicates based on URL
    seen_urls = set()
    unique_results = []
    
    for result in all_results:
        url = result.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)
    
    logger.info(f"Total unique results: {len(unique_results)}")
    return unique_results

# Example usage and testing
if __name__ == "__main__":
    async def test_search():
        # Test queries
        test_queries = [
            "AI in healthcare",
            "machine learning in hospitals",
            "artificial intelligence medical diagnosis"
        ]
        
        results = await search_multiple_queries(test_queries)
        
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results[:10], 1):  # Show first 10 results
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print()
        
        # Return results in the expected format for Team 4
        return results
    
    # Run the test
    asyncio.run(test_search())
