from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import OPENROUTER_API_KEY, BASE_URL, GIGACHAT_CREDENTIALS

from langchain_community.chat_models.gigachat import GigaChat

llm = ChatOpenAI(
    temperature=0,
    base_url=BASE_URL,
    api_key=OPENROUTER_API_KEY,
    model="huggingfaceh4/zephyr-7b-beta:free",
)
nodes_data = {
    "catalog": {"description": "Каталог, описание товаров."},
    "order": {"description": "Оформление заказа"},
    "company_data": {"description": "Ответы на вопросы о компании."},
    "route_creator": {"description": "Наше местоположение. Создание маршрута"},
}
action_extractor_prompt_template = """Выдели действие из сообщения пользователя и данные которые он предоставил. К одной из нод. Ноды: {nodes}. Если действий несколько, раздели их и для каждого действия определи данные. Действуй строго по инструкции. При отсутствии данных пиши только действие.
                 Reference для тебя: Пользователь: Я хочу сделать заказать цветы ко мне домой на юбилейную 22 в городе Пышма в 10 утра завтра. Сколько будут стоить хризантемы за штуку стоить?
                 Твой ответ: Действие: Заказ цветов. Данные: Город: Пышма. Адрес: Юбилейная 22. Время: 10AM. Дата: Завтра. Нода: order\n Действие: Запрос стоимости. Данные: Объект: Хризантемы. Количество: 1. Нода: catalog.
                 
                 Ответь на это сообщение:
                 Сообщение пользователя: {input}"""

action_extractor_prompt = PromptTemplate(
    input_variables=["input", "nodes"], template=action_extractor_prompt_template
)

gigachat = GigaChat(
    scope="GIGACHAT_API_PERS",
    credentials=GIGACHAT_CREDENTIALS,
    verify_ssl_certs=False,
)

for chunk in gigachat.stream(
    action_extractor_prompt.invoke(
        input={
            "input": "Здравтствуйте! Что вы можете мне предложить?",
            "nodes": str(nodes_data),
        }
    )
):
    print(chunk)


# prompt = PromptTemplate(input_variables=["input"], template="{input}")

# chain = prompt | llm

# print(chain.invoke("Hello! What you can do?"))
