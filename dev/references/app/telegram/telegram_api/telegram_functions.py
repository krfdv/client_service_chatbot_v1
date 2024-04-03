from aiogram import Bot
import os

app = Bot(os.environ["TELEGRAM_BOT_TOKEN"])


async def send_message_to_user(id: str, message: str):
    answ = await app.send_message(id, message)
    return answ
