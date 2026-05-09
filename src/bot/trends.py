from __future__ import annotations

import random
import feedparser
import praw

GOOGLE_NEWS_AI_RSS = "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en"
REDDIT_SUBREDDITS = ["ArtificialInteligence", "MachineLearning", "singularity", "OpenAI"]


def fetch_trending_ai_topics(reddit_client_id: str, reddit_client_secret: str, reddit_user_agent: str, max_topics: int = 15) -> list[str]:
    topics: list[str] = []

    reddit = praw.Reddit(
        client_id=reddit_client_id,
        client_secret=reddit_client_secret,
        user_agent=reddit_user_agent,
    )

    for sub in REDDIT_SUBREDDITS:
        for post in reddit.subreddit(sub).hot(limit=8):
            title = (post.title or "").strip()
            if title and title not in topics:
                topics.append(title)

    parsed = feedparser.parse(GOOGLE_NEWS_AI_RSS)
    for entry in parsed.entries[:20]:
        title = getattr(entry, "title", "").strip()
        if title and title not in topics:
            topics.append(title)

    random.shuffle(topics)
    return topics[:max_topics]
