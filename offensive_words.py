from aiogram import types
from ban_logic import ban_user_if_necessary

bad_words = ["плохой", "тупой", "худой"]

async def process_offensive_message(message, user_violations):
    if message.content_type == types.ContentType.TEXT:
        if any(bad_word in message.text.lower() for bad_word in bad_words):
            user_id = message.from_user.id
            chat_id = message.chat.id
            if user_id not in user_violations:
                user_violations[user_id] = 1
            else:
                user_violations[user_id] += 1
            await ban_user_if_necessary(user_violations, user_id, chat_id)
            await message.reply("Пиши норм")
