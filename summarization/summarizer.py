import asyncio
import aiohttp
import json

# Default configuration for a local LLM (e.g., Ollama)
# You can change this to point to a different API if needed.
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3" # Or "mistral", "gemma", etc.

async def summarize_sources(contents, topic):
    """
    Summarizes a list of documents relative to a specific topic using an LLM.

    Args:
        contents (list): A list of dictionaries containing document data.
                         Must contain 'content' and 'url' keys.
        topic (str): The topic to focus the summary on.

    Returns:
        list: A list of dictionaries with 'url', 'summary', and 'confidence_score'.
    """
    summaries = []
    
    # Create an async session
    async with aiohttp.ClientSession() as session:
        tasks = []
        for doc in contents:
            if not doc.get('content'):
                continue
                
            task = _generate_summary(session, doc, topic)
            tasks.append(task)
        
        # Run all summary tasks concurrently
        results = await asyncio.gather(*tasks)
        
        # Filter out any None results (failed summaries)
        summaries = [res for res in results if res is not None]
        
    return summaries

async def _generate_summary(session, doc, topic):
    """
    Helper function to call the LLM API for a single document.
    """
    url = doc.get('url', 'Unknown URL')
    text = doc.get('content', '')[:3000] # Truncate text to avoid context limit issues
    
    prompt = f"""
    Explain the following text in simple language, focusing on the topic: "{topic}".
    Provide a concise summary of the key points.
    
    Text:
    {text}
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        async with session.post(OLLAMA_API_URL, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                summary_text = data.get('response', '').strip()
                
                # We mock a confidence score here since most simple LLM APIs don't return one directly for generation
                # In a real production system, you might ask the model to rate its own confidence.
                confidence = 0.85 
                
                return {
                    "url": url,
                    "summary": summary_text,
                    "confidence_score": confidence
                }
            else:
                print(f"Failed to summarize {url}: Status {response.status}")
                return None
    except Exception as e:
        print(f"Error summarizing {url}: {e}")
        # Fallback for demonstration if API is not running
        return {
            "url": url,
            "summary": "Error: Could not connect to summarization model. Is Ollama running?",
            "confidence_score": 0.0
        }

if __name__ == "__main__":
    # Test data
    sample_contents = [
        {
            "url": "http://example.com/1",
            "content": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming."
        },
        {
            "url": "http://example.com/2",
            "content": "Rust is a multi-paradigm, general-purpose programming language. Rust emphasizes performance, type safety, and concurrency. Rust enforces memory safety—that is, that all references point to valid memory—without requiring the use of a garbage collector or reference counting present in other memory-safe languages."
        }
    ]
    
    topic = "Programming Languages"
    
    print(f"Summarizing {len(sample_contents)} documents on topic: '{topic}'...")
    
    # Run the async function
    summaries = asyncio.run(summarize_sources(sample_contents, topic))
    
    print("\n--- Results ---")
    print(json.dumps(summaries, indent=2))
