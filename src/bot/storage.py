from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class TweetHistoryStore:
    def __init__(self, path: str = "data/tweet_history.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"tweets": []})

    def _read(self) -> dict[str, Any]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, payload: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add_tweet(self, tweet_text: str, topic: str, tweet_id: str | None = None) -> None:
        payload = self._read()
        payload["tweets"].append(
            {
                "tweet": tweet_text,
                "topic": topic,
                "tweet_id": tweet_id,
            }
        )
        self._write(payload)

    def recent_tweets(self, limit: int = 200) -> list[str]:
        payload = self._read()
        items = payload.get("tweets", [])
        return [i["tweet"] for i in items[-limit:] if "tweet" in i]

    def is_duplicate(self, candidate: str) -> bool:
        norm = " ".join(candidate.lower().split())
        for tweet in self.recent_tweets():
            if norm == " ".join(tweet.lower().split()):
                return True
        return False
