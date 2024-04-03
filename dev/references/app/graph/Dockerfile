FROM python:3.11.8

WORKDIR /app

ADD graph_api.py .
ADD graph.py .
ADD framework.py .
ADD products.json .
ADD graph_building.py .



COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 3311

CMD ["uvicorn", "graph_api:app", "--host", "0.0.0.0", "--port", "3311"]