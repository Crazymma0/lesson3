from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from decouple import config
from ban_logic import ban_user_if_necessary
from offensive_words import process_offensive_message

bot = Bot(token=config('TOKEN'))
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

class FormStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_email = State()

@dp.message_handler(Command('start'))
async def start(message: types.Message):
    await message.reply("Давайте начнем заполнение анкеты!\nВведите ваше имя:")
    await FormStates.waiting_for_name.set()

@dp.message_handler(state=FormStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FormStates.waiting_for_age.set()
    await message.reply("Введите ваш возраст:")

@dp.message_handler(state=FormStates.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await FormStates.waiting_for_email.set()
    await message.reply("Введите ваш email:")

@dp.message_handler(state=FormStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    survey_text = f"Анкета:\nИмя: {data['name']}\nВозраст: {data['age']}\nEmail: {data['email']}"

    await bot.send_message(message.chat.id, survey_text)

    await state.finish()
    await message.reply("Спасибо за заполнение анкеты!")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text_message(message: types.Message):
    user_violations = {}
    await ban_user_if_necessary(user_violations, message.from_user.id, message.chat.id)
    await process_offensive_message(message, user_violations)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
