from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    groq_api_key: str
    groq_model: str
    x_email: str
    x_username: str
    x_password: str
    post_times_utc: list[str]
    max_tweet_length: int = 240

    @staticmethod
    def from_env() -> "Settings":
        settings = Settings(
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            groq_model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            x_email=os.getenv("X_EMAIL", ""),
            x_username=os.getenv("X_USERNAME", ""),
            x_password=os.getenv("X_PASSWORD", ""),
            post_times_utc=[
                x.strip()
                for x in os.getenv(
                    "POST_TIMES_UTC",
                    "08:00,11:00,14:00,17:00,20:00"
                ).split(",")
                if x.strip()
            ],
        )

        settings.validate()
        return settings

    def validate(self) -> None:
        required = {
            "GROQ_API_KEY": self.groq_api_key,
            "X_EMAIL": self.x_email,
            "X_USERNAME": self.x_username,
            "X_PASSWORD": self.x_password,
        }

        missing = [k for k, v in required.items() if not v]

        if missing:
            raise ValueError(
                f"Missing required env vars: {', '.join(missing)}"
            )
