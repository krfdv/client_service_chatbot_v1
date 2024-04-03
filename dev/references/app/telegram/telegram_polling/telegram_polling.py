from aiogram import Bot, Dispatcher
from aiogram.types import Message
import httpx
import json
import os

dp = Dispatcher()


async def send_to_graph(id: str, message: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://graph:3311/send_message",
            params={"id": id, "message": message},
        )
    answer = (
        response.json()["answer"] + "\n\n" + unpack_buttons(response.json()["buttons"])
    )

    return answer


def unpack_buttons(buttons: list) -> str:
    answer = ""
    for button in buttons:
        answer += " -" + button + "\n"
    return answer


@dp.message()
async def message_handler(message: Message):
    # with open('logs.txt', 'a') as f:
    #     f.write(str(message.from_user.id) + " " + message.text)
    #     f.write('\n')
    answer = await send_to_graph(str(message.from_user.id), message.text)
    return await message.answer(answer)


async def main(token: str = os.environ["TELEGRAM_BOT_TOKEN"]):
    import logging
    import sys

    app = Bot(token)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(app)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
