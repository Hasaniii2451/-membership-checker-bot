import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import create_db

from handlers import start
from handlers import check
from handlers import admin


async def main():

    await create_db()

    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(check.router)
    dp.include_router(admin.router)

    print("Bot started...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
