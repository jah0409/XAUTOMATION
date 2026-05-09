from __future__ import annotations

import random
import feedparser

GOOGLE_NEWS_AI_RSS = "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en"
STATIC_AI_TOPICS = [
    "AI agents replacing repetitive workflows",
    "Small language models on-device",
    "Multimodal AI in everyday apps",
    "Open-source AI vs closed models",
    "AI copilots for software teams",
    "AI regulation and innovation balance",
    "Synthetic data for model training",
    "RAG systems in production",
]


def fetch_trending_ai_topics(max_topics: int = 15) -> list[str]:
    topics: list[str] = []

    parsed = feedparser.parse(GOOGLE_NEWS_AI_RSS)
    for entry in parsed.entries[:20]:
        title = getattr(entry, "title", "").strip()
        if title and title not in topics:
            topics.append(title)

    for topic in STATIC_AI_TOPICS:
        if topic not in topics:
            topics.append(topic)

    random.shuffle(topics)
    return topics[:max_topics]
