import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import Executor

from bot.leetcode_bot import LeetCodeBot


class LeetCodeTelegramBot:
    def __init__(self,
                 api_token: str,
                 proxy: str,
                 bot: LeetCodeBot):
        self._bot = bot
        self._telegram_bot = Bot(token=api_token, proxy=proxy)
        self._dispatcher = Dispatcher(self._telegram_bot, loop=asyncio.get_running_loop())

    async def start(self):
        self._dispatcher.register_message_handler(
            callback=self._send_welcome,
            commands=['start', 'help']
        )
        self._dispatcher.register_message_handler(
            callback=self._configure,
            commands=['configure']
        )

        await self._bot.start(lambda chat, message: self._telegram_bot.send_message(
            chat_id=chat,
            text=message
        ))
        await self._start_polling()

    async def _send_welcome(self, message: types.Message):
        await message.reply("Hi!\nI'm LeetCode notify bot. Use /configure [usernames] to start following users")

    async def _configure(self, message: types.Message):
        user_names = message.text.split(' ')[1:-1]
        if len(user_names) > 0:
            await self._bot.configure(user_names=user_names, chat_id=str(message.chat.id))
            await message.reply("Configured")
        else:
            await message.reply("Incorrect params")

    # noinspection PyProtectedMember
    async def _start_polling(self):
        executor = Executor(self._dispatcher, skip_updates=False)
        executor._prepare_polling()

        loop: asyncio.AbstractEventLoop = executor.loop

        try:
            await executor._startup_polling()
            await self._dispatcher.start_polling()
        except (KeyboardInterrupt, SystemExit):
            loop.stop()
            pass
        finally:
            await executor._shutdown_polling()
