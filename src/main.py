import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(F.text == "/start")
async def start_handler(message: Message):
    """ Start handler """
    await message.answer("Hello, world!")


async def main():
    print("🚀 Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        print("🛑 Bot stopped")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
