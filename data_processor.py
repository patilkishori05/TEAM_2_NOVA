import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove non-printable chars
    text = re.sub(r"[^\x20-\x7E]", " ", text)

    # Remove very short junk tokens
    text = re.sub(r"\b\w{1,2}\b", " ", text)

    # Normalize again
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_content_batch(contents):
    """
    contents:
    [{"url": "...", "raw_text": "..."}]

    returns:
    [{"url": "...", "clean_text": "..."}]
    """

    cleaned = []

    for item in contents:
        cleaned_text = clean_text(item.get("raw_text", ""))

        cleaned.append({
            "url": item["url"],
            "clean_text": cleaned_text
        })

    return cleaned
