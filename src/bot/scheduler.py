from __future__ import annotations

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import Settings
from .generator import TweetGenerator
from .storage import TweetHistoryStore
from .trends import fetch_trending_ai_topics
from .twitter_client import XWebClient


class BotScheduler:
    def __init__(self, settings: Settings, logger: logging.Logger) -> None:
        self.settings = settings
        self.logger = logger
        self.store = TweetHistoryStore()
        self.generator = TweetGenerator(settings.groq_api_key, settings.groq_model, settings.max_tweet_length)
        self.x_client = XWebClient(settings.x_email, settings.x_username, settings.x_password)

    def run_once(self) -> None:
        topics = fetch_trending_ai_topics()
        recent = self.store.recent_tweets(200)

        chosen_tweet = ""
        chosen_topic = ""
        for topic in topics:
            candidate = self.generator.generate(topic, recent)
            if candidate and not self.store.is_duplicate(candidate):
                chosen_tweet = candidate
                chosen_topic = topic
                break

        if not chosen_tweet:
            self.logger.warning("No unique tweet generated.")
            return

        post_id = self.x_client.post_tweet(chosen_tweet)
        self.store.add_tweet(chosen_tweet, chosen_topic, post_id)
        self.logger.info("Posted: %s", chosen_tweet)

    def start(self) -> None:
        scheduler = BlockingScheduler(timezone="UTC")
        for hhmm in self.settings.post_times_utc:
            hour, minute = hhmm.split(":", maxsplit=1)
            scheduler.add_job(self.run_once, CronTrigger(hour=int(hour), minute=int(minute)))
            self.logger.info("Scheduled at %s UTC", hhmm)
        scheduler.start()
