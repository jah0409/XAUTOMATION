from __future__ import annotations

import random
import time

from playwright.sync_api import sync_playwright


class XWebClient:
    def __init__(self, email: str, username: str, password: str) -> None:
        self.email = email
        self.username = username
        self.password = password

    def delay(self, a=1.5, b=3.5):
        time.sleep(random.uniform(a, b))

    def post_tweet(self, text: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                ],
            )

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 900},
            )

            page = context.new_page()

            page.goto("https://x.com/login", timeout=120000)

            self.delay(5, 8)

            page.wait_for_selector('input', timeout=120000)

            inputs = page.locator("input")
            first_input = inputs.nth(0)

            first_input.fill(self.email)

            self.delay()

            page.keyboard.press("Enter")

            self.delay(4, 6)

            # Optional username verification
            try:
                verify_input = page.locator('input').nth(0)

                if verify_input.is_visible(timeout=5000):
                    verify_input.fill(self.username)
                    self.delay()
                    page.keyboard.press("Enter")
                    self.delay(3, 5)
            except:
                pass

            password_input = page.locator('input[type="password"]')

            password_input.wait_for(timeout=120000)

            password_input.fill(self.password)

            self.delay()

            page.keyboard.press("Enter")

            self.delay(8, 12)

            page.goto("https://x.com/compose/post", timeout=120000)

            self.delay(5, 8)

            tweet_box = page.locator('div[role="textbox"]')

            tweet_box.wait_for(timeout=120000)

            tweet_box.fill(text)

            self.delay(2, 4)

            post_button = page.locator('button[data-testid="tweetButtonInline"]')

            post_button.click()

            self.delay(5, 8)

            browser.close()

            return "posted"
