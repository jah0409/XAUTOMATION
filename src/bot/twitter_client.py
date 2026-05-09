from __future__ import annotations

import random
import time
from playwright.sync_api import sync_playwright


class XWebClient:
    def __init__(self, email: str, username: str, password: str) -> None:
        self.email = email
        self.username = username
        self.password = password

    @staticmethod
    def _human_type(locator, text: str) -> None:
        for ch in text:
            locator.type(ch, delay=random.randint(40, 120))

    @staticmethod
    def _random_delay(low: float = 0.8, high: float = 2.2) -> None:
        time.sleep(random.uniform(low, high))

    def post_tweet(self, text: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded")
            self._random_delay()

            user_input = page.locator('input[autocomplete="username"]')
            user_input.wait_for(timeout=20000)
            self._human_type(user_input, self.email)
            page.keyboard.press("Enter")
            self._random_delay()

            maybe_username = page.locator('input[data-testid="ocfEnterTextTextInput"]')
            if maybe_username.count() > 0:
                self._human_type(maybe_username.first, self.username)
                page.keyboard.press("Enter")
                self._random_delay()

            pass_input = page.locator('input[name="password"]')
            pass_input.wait_for(timeout=20000)
            self._human_type(pass_input, self.password)
            page.keyboard.press("Enter")
            self._random_delay(2.0, 4.0)

            page.goto("https://x.com/compose/post", wait_until="domcontentloaded")
            composer = page.locator('div[data-testid="tweetTextarea_0"]')
            composer.wait_for(timeout=20000)
            composer.click()
            self._human_type(composer, text)
            self._random_delay()

            page.locator('button[data-testid="tweetButton"]').click()
            self._random_delay(2.0, 3.0)

            browser.close()
            return "posted_via_playwright"
