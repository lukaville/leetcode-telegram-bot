import asyncio
import logging
import os

from bot.leetcode_bot import LeetCodeBot
from bot.leetcode_telegram_bot import LeetCodeTelegramBot

DEFAULT_CONFIG_PATH = '/data/config.json'


async def main():
    logging.basicConfig(level=logging.INFO)

    token = os.environ['TELEGRAM_API_TOKEN']
    bot = LeetCodeBot(config_path=DEFAULT_CONFIG_PATH)
    telegram_bot = LeetCodeTelegramBot(api_token=token, bot=bot)
    await telegram_bot.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
