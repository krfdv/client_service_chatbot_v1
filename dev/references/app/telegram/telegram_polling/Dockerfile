FROM python:3.11.8

WORKDIR /app

ADD telegram_polling.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

ENV TELEGRAM_BOT_TOKEN=""


CMD ["python", "telegram_polling.py"]

