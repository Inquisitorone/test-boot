import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import os

TELEGRAM_API_TOKEN = os.getenv("8061299708:AAGNWggA1u1nxosvOimH2k53FeQ--aXcReE")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    city = State()
    vin = State()
    dlink = State()
    language = State()
    comment = State()
    confirm = State()

@dp.message_handler(commands='start')
async def start_cmd(message: types.Message):
    await message.answer("Введите город:")
    await Form.city.set()

@dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введите VIN:")
    await Form.vin.set()

@dp.message_handler(state=Form.vin)
async def process_vin(message: types.Message, state: FSMContext):
    await state.update_data(vin=message.text)
    await message.answer("Введите версию Dlink:")
    await Form.dlink.set()

@dp.message_handler(state=Form.dlink)
async def process_dlink(message: types.Message, state: FSMContext):
    await state.update_data(dlink=message.text)
    await message.answer("Введите язык (UA или RU):")
    await Form.language.set()

@dp.message_handler(state=Form.language)
async def process_language(message: types.Message, state: FSMContext):
    await state.update_data(language=message.text)
    await message.answer("Введите комментарий (или '-' если нет):")
    await Form.comment.set()

@dp.message_handler(state=Form.comment)
async def process_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    summary = f"""
📋 <b>Заявка:</b>
Город: {data['city']}
VIN: {data['vin']}
Версия Dlink: {data['dlink']}
Язык: {data['language']}
Комментарий: {data['comment']}
"""
    await message.answer(summary, parse_mode="HTML")
    await message.answer("Подтвердите заявку? (да/нет)")
    await Form.confirm.set()

@dp.message_handler(state=Form.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.answer("Заявка подтверждена. Спасибо!")
    else:
        await message.answer("Заявка отменена.")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
