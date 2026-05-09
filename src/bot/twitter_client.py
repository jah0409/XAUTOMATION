from __future__ import annotations

import random
import time

from playwright.sync_api import sync_playwright


class XWebClient:
    def __init__(self, email: str, username: str, password: str) -> None:
        self.email = email
        self.username = username
        self.password = password

    def human_delay(self, a: float = 1.0, b: float = 2.5) -> None:
        time.sleep(random.uniform(a, b))

    def post_tweet(self, text: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto("https://x.com/i/flow/login", timeout=60000)

            self.human_delay(2, 4)

            # Username/email input
            page.locator('input[name="text"]').wait_for(timeout=60000)
            page.locator('input[name="text"]').fill(self.email)

            self.human_delay()

            page.keyboard.press("Enter")

            self.human_delay(3, 5)

            # Sometimes X asks for username confirmation
            try:
                username_input = page.locator('input[data-testid="ocfEnterTextTextInput"]')
                if username_input.is_visible(timeout=5000):
                    username_input.fill(self.username)
                    self.human_delay()
                    page.keyboard.press("Enter")
                    self.human_delay(2, 4)
            except:
                pass

            # Password input
            page.locator('input[name="password"]').wait_for(timeout=60000)
            page.locator('input[name="password"]').fill(self.password)

            self.human_delay()

            page.keyboard.press("Enter")

            self.human_delay(5, 8)

            # Open compose box
            page.goto("https://x.com/compose/post", timeout=60000)

            self.human_delay(4, 6)

            tweet_box = page.locator('div[role="textbox"]')
            tweet_box.wait_for(timeout=60000)

            tweet_box.fill(text)

            self.human_delay(2, 4)

            post_button = page.locator('button[data-testid="tweetButtonInline"]')
            post_button.click()

            self.human_delay(5, 8)

            browser.close()

            return "posted"
