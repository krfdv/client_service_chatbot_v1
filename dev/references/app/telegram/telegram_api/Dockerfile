FROM python:3.11.8

WORKDIR /app

ADD telegram_api.py .
ADD telegram_functions.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

ENV TELEGRAM_BOT_TOKEN="6886579173:AAEp_KAV2cLTHBQ-X__3hyUKxLMztmjYFaY"
EXPOSE 3310

CMD ["uvicorn", "telegram_api:app", "--host", "0.0.0.0", "--port", "3310"]

