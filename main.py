import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "8061299708:AAGNWggA1u1nxosvOimH2k53FeQ--aXcReE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я простой Telegram-бот.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)