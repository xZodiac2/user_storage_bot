from aiogram import Bot, Dispatcher
import asyncio
from handlers import router
from database import init_db


async def main():
    await init_db()

    bot = Bot("6625817529:AAEHfJK7QXcr_YFg-DXVAhc4c1BvFiU4lyI")
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())