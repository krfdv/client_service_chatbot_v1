endpoints = {}
from langgraph.graph import Graph, END
import re


####### Main functions #######
def create_node(workspace: Graph, node: callable, name: str, endpoints=endpoints):
    """
    Добавляет данные о ноде в словарь endpoints

    Создаёт обертку для ноды: node_end. Добавляет кнопки в ответ.

    """
    if name not in endpoints:
        endpoints[name] = {}

    end_node = name + "_end"
    workspace.add_node(name, node)
    workspace.add_node(
        end_node,
        lambda state: {"origin": name, "buttons": _get_buttons(name, endpoints)},
    )
    workspace.add_edge(end_node, END)
    workspace.add_edge(name, end_node)


def create_edge(
    origin: str,
    endpoint: str,
    aliases: list,
    endpoints=endpoints,
):
    """
    Добавляет в словарь endpoints ребро а также добавляет в него aliases

    """
    if origin not in endpoints:
        endpoints[origin] = {endpoint: []}
    endpoints[origin][endpoint] = aliases
    return endpoints


def create_validator(workspace: Graph, endpoints=endpoints):
    # Создание валидатора
    def validate(state):
        if state["origin"] == None:
            return "__init__"
        # Проверка кнопок.
        buttons = endpoints[state["origin"]]
        for endpoint, alliases in buttons.items():
            if state["input"] in alliases:
                return endpoint
        user_input = state["input"]
        origin = state["origin"]

        # Обработка номера телефона
        if origin == "phone_number":
            match = re.match(
                r"\+?[78][-\s]?\(?\d{3}\)?[\s-]?\d{3}[-\s]?\d{2}[\s-]?\d{2}", user_input
            )
            if match:
                tel = "8" + "".join(filter(str.isdigit, match.group()))[1:]
                user_input = "+7 ({}) {}-{}-{}".format(
                    tel[1:4], tel[4:7], tel[7:9], tel[9:11]
                )
                return {"input": user_input, "endpoint": "phone_number"}
            else:
                return {"input": user_input, "endpoint": "phone_validate"}

    workspace.add_node("validate", validate)

    def _classify(state):
        return state["endpoint"]

    workspace.add_conditional_edges(_classify, _create_node_map())


def compile(workspace: Graph):
    workspace.entry_point = "validate"
    return workspace.compile()


###### HELPERS ######
def _get_buttons(origin, endpoints=endpoints):
    if origin not in endpoints:
        return []
    buttons = []
    for aliases in endpoints[origin].values():
        buttons = buttons + aliases
    return buttons


def _create_node_map(endpoints=endpoints):
    node_map = {}
    for node in endpoints.keys():
        node_map[node] = node

    node_map["validate"] = "validate"
    return node_map
