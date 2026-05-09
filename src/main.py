import argparse

from bot.config import Settings
from bot.logger import setup_logging
from bot.scheduler import BotScheduler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run one posting cycle")
    args = parser.parse_args()

    logger = setup_logging()
    settings = Settings.from_env()
    bot = BotScheduler(settings, logger)

    if args.once:
        bot.run_once()
        return

    bot.start()


if __name__ == "__main__":
    main()
