from aiogram import Bot
from decouple import config

bot = Bot(token=config('TOKEN'))

async def ban_user_if_necessary(user_violations, user_id, chat_id):
    if user_id in user_violations and user_violations[user_id] >= 2:
        await bot.kick_chat_member(chat_id, user_id)
