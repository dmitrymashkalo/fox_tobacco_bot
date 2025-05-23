import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.routers import routers
from src.config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def main():
    print("🚀 Bot started")
    try:
        for router in routers:
            dp.include_router(router)

        await dp.start_polling(bot)
    finally:
        print("🛑 Bot stopped")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
