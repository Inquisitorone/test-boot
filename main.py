
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import os

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("Set TELEGRAM_API_TOKEN environment variable.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    city = State()
    vin = State()
    dlink = State()
    language = State()
    comment = State()
    confirm = State()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Введите город:")
    await Form.city.set()


@dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введите VIN код:")
    await Form.vin.set()


@dp.message_handler(state=Form.vin)
async def process_vin(message: types.Message, state: FSMContext):
    await state.update_data(vin=message.text)
    await message.answer("Введите версию Dlink:")
    await Form.dlink.set()


@dp.message_handler(state=Form.dlink)
async def process_dlink(message: types.Message, state: FSMContext):
    await state.update_data(dlink=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("UA", "RU")
    await message.answer("Выберите язык мультимедиа:", reply_markup=keyboard)
    await Form.language.set()


@dp.message_handler(state=Form.language)
async def process_language(message: types.Message, state: FSMContext):
    await state.update_data(language=message.text)
    await message.answer("Введите комментарий (или напишите 'Пропустить'):", reply_markup=types.ReplyKeyboardRemove())
    await Form.comment.set()


@dp.message_handler(state=Form.comment)
async def process_comment(message: types.Message, state: FSMContext):
    comment = message.text if message.text.lower() != "пропустить" else "Без комментария"
    await state.update_data(comment=comment)
    data = await state.get_data()

    summary = (
        f"📋 <b>Заявка:</b>
"
        f"🏙️ Город: {data['city']}
"
        f"🔍 VIN: {data['vin']}
"
        f"💾 Версия Dlink: {data['dlink']}
"
        f"🌐 Язык: {data['language']}
"
        f"📝 Комментарий: {data['comment']}"
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Подтвердить", "Отмена")
    await message.answer(summary, parse_mode="HTML", reply_markup=keyboard)
    await Form.confirm.set()


@dp.message_handler(state=Form.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text == "Подтвердить":
        await message.answer("✅ Заявка принята. Спасибо!", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("❌ Заявка отменена.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
