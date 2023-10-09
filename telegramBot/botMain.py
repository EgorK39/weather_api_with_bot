import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from handlers import messages

import os

from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    bot = Bot(os.getenv('token'))
    dp = Dispatcher()
    dp.include_routers(messages.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, polling_timeout=8)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
