from fastapi import Request, FastAPI
from telegram_functions import send_message_to_user

app = FastAPI()


@app.post("/send_message")
async def send_data(request: Request):
    data = await request.json()
    id = data["id"]
    text = data["message"]
    await send_message_to_user(id, text)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=3310)
