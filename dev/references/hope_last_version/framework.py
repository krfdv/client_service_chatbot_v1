from langgraph.graph import StateGraph, END
import re
from typing import Annotated, Union, Sequence, TypedDict, List


class AgentState(TypedDict):
    id: str | None
    input: str
    output: str
    origin: List[str]
    go_to: List[str]


example = {
    "node_name": {
        "description": "",
        "outgoing_nodes": [
            {"name": "", "button": "", "description": "", "aliases": []}
        ],
        "distance": int,
    }
}


class GraphRenewed:
    def __init__(self):
        self.workspace = StateGraph(AgentState)
        self.node_info = {}

    def create_entry_point(self, name):
        self.workspace.set_entry_point(name)

    def create_manager(self):

        def manager(state):
            # Проверка соответствия уровня. Спуск на уровень ниже
            if len(state["origin"]) > 1:
                go_to = state["origin"].pop(0)
                return state["go_to":go_to]
            # Проверка buttons
            if state["input"] in self.node_info[state["origin"]]["outgoing_nodes"]:
                return state["go_to" : state["input"]]
            return self.node_info[state["origin"]]["name"]

        self.workspace.add_node("manager", manager)

    def create_node(self, node, name, description):
        if name not in self.node_info:
            self.workspace.add_node(name, node)
            self.node_info[name] = {"description": description, "outgoing_nodes": []}
        else:
            return f"Node {name} already exists"

    def create_edge(
        self,
        first_node,
        second_node,
        button,
        descrition=None,
        aliases=None,
        validator: callable = None,
    ):
        self.node_info[first_node]["outgoing_nodes"].append(
            {
                "name": second_node,
                "button": button,
                "description": descrition,
                "aliases": aliases,
                "validator": validator,
            }
        )
