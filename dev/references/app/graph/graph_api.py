from fastapi import FastAPI
import graph as graph

app = FastAPI()

origins = graph.OriginDB()


@app.get("/send_message")
async def send_data(id, message):
    answer = graph.run(id, message, origins)
    return answer
