from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from decouple import config
from ban_logic import ban_user_if_necessary
from offensive_words import process_offensive_message

bot = Bot(token=config('TOKEN'))
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(Command('start'))
async def start(message: types.Message):
    await message.reply("Вы были успешно зарегистрированы!")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text_message(message: types.Message):
    user_violations = {}
    await ban_user_if_necessary(user_violations, message.from_user.id, message.chat.id)
    await process_offensive_message(message, user_violations)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
