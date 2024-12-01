from aiogram import Bot, Dispatcher, types

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers import router

import asyncio
from config import *

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
	# Бот начинает работать
	dp.include_router(router)
	print("started")
	await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())