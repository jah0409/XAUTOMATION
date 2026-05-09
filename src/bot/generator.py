from __future__ import annotations

from groq import Groq


class TweetGenerator:
    def __init__(self, api_key: str, model: str, max_chars: int = 240) -> None:
        self.client = Groq(api_key=api_key)
        self.model = model
        self.max_chars = max_chars

    def generate(self, topic: str, recent_tweets: list[str]) -> str:
        recent_block = "\n".join(f"- {t}" for t in recent_tweets[-20:]) or "None"
        prompt = (
            "Write exactly one tweet for X about AI. Sound like a real human with curiosity-driven tone, "
            "lightly contrarian or insight-led when useful, but not clickbait spam. "
            "No emojis unless truly helpful. Max length 240 chars. Output only tweet text.\n\n"
            f"Topic: {topic}\n"
            f"Avoid duplicating these:\n{recent_block}\n"
        )
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
        )
        text = completion.choices[0].message.content.strip()
        if len(text) > self.max_chars:
            text = text[: self.max_chars - 1].rstrip() + "…"
        return text
