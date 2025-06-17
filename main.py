import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "8061299708:AAGNWggA1u1nxosvOimH2k53FeQ--aXcReE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я Telegram-бот и я работаю 😊")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)