# report_generator.py
from datetime import datetime

async def generate_report(summaries, topic, length="short", format="md"):
    """
    summaries: list of dicts or strings
    topic: research topic
    length: short | medium | long
    format: md | pdf | json
    """

    date = datetime.now().strftime("%Y-%m-%d")

    # Adjust number of points based on length
    if length == "short":
        selected = summaries[:3]
    elif length == "medium":
        selected = summaries[:5]
    else:
        selected = summaries

    report = {
        "title": f"Autonomous Web Research Report",
        "topic": topic,
        "date": date,
        "introduction": f"This report presents automated research findings on the topic: {topic}.",
        "findings": selected,
        "conclusion": f"The research highlights key insights related to {topic} based on web data."
    }

    return report
