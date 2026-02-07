import asyncio
from content_extractor import extract_content_batch
from data_processor import clean_content_batch


urls = [
    {"url": "https://example.com"},
    {"url": "https://www.wikipedia.org"},
]


async def main():
    print("Fetching content...")

    raw = await extract_content_batch(urls)

    print("Cleaning content...")
    cleaned = clean_content_batch(raw)

    for item in cleaned:
        print("\n==============================")
        print("URL:", item["url"])
        print("TEXT SAMPLE:")
        print(item["clean_text"][:400])


if __name__ == "__main__":
    asyncio.run(main())
