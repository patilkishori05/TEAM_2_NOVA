import aiohttp
import asyncio
from bs4 import BeautifulSoup
from readability import Document


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


async def fetch(session, url):
    try:
        async with session.get(url, headers=HEADERS, timeout=20) as resp:
            if resp.status == 200:
                return await resp.text()
            else:
                return None
    except Exception:
        return None


def extract_main_text(html: str) -> str:
    """
    Uses readability to isolate main article content,
    then BeautifulSoup to extract clean text.
    """
    if not html:
        return ""

    doc = Document(html)
    main_html = doc.summary(html_partial=True)

    soup = BeautifulSoup(main_html, "html.parser")

    # Remove junk tags
    for tag in soup(["script", "style", "noscript", "iframe", "svg"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return text


async def extract_content_batch(results):
    """
    results: list of dicts like:
    [{"url": "https://example.com"}, ...]

    returns:
    [{"url": "...", "raw_text": "..."}]
    """

    urls = [r["url"] for r in results]
    output = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

    for url, html in zip(urls, pages):
        raw_text = extract_main_text(html)
        output.append({
            "url": url,
            "raw_text": raw_text
        })

    return output
