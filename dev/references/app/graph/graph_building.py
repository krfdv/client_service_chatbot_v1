import operator
from langgraph.graph import StateGraph, END
import asyncio
from typing import Annotated, Union, Sequence, TypedDict, List
from langchain_core.runnables import RunnableLambda
from framework import create_edge, create_node, compile
from langchain.prompts import PromptTemplate
import json
import re


###### INITIALIZATION
class BotState(TypedDict):
    input: str

    file: bytes

    answers: Annotated[List[str], operator.add]

    buttons: list

    origin: str

    endpoint: str


workspace = StateGraph(BotState)

###### LOGIC/EDGES
create_edge(
    "__init__",
    "menu",
    ["далее", "начать"],
)
create_edge("menu", "description", ["Чатбот", "Автоматизация"])
create_edge(
    "description", "phone_number", ["Отлично!", "Это мне нужно", "Заказать", "Далее"]
)
create_edge(
    "phone_number",
    "final",
    ["Пропустить"],
)
create_edge("final", "menu", ["далее", "продолжить"])


###### FUNCTIONS
def menu(state):
    return {
        "answers": ["Добро пожаловать! Осмотритесь тут. Предлагаю вам выбрать товары:"]
    }


def description(state):
    with open(
        "products.json", "r", encoding="utf-8"
    ) as products:  # открываем файл на чтение
        data = json.load(products)  # загружаем из файла данные в словарь data
    return {"answers": [data[state["input"]]]}


###### CREATING_NODES
create_node(workspace, menu, "menu")
create_node(workspace, description, "description")
create_node(
    workspace,
    RunnableLambda(lambda state: {"answers": ["Введите номер телефона:"]}),
    "phone_number",
)
create_node(
    workspace,
    RunnableLambda(
        lambda state: {
            "answers": [
                f"Отлично. Мы вскоре позвоним вам на номер {state['input']}. \nДо встречи!"
            ]
        }
    ),
    "final",
)

create_node(
    workspace,
    RunnableLambda(
        lambda state: {
            "answers": [
                'Это первая, пробная версия бота. Нажмите "далее", что бы активировать его.'
            ]
        }
    ),
    "__init__",
)

###### COMPILING
graph = compile(workspace)
