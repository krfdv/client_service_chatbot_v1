import langgraph

nodes = {}


def create_node(node_name: str, node: callable):
    if node_name not in nodes:
        nodes[node_name] = {}
    nodes[node_name]["node"] = node


def create_verify(node_name: str, verify: callable):
    """Задача: сделать возможным проверить соответствие данных для того, чтобы убедиться в том, что это нужная нода.
    verify - функция которая принимает строку и возвращается число от 0 до 1
    """
    if node_name not in nodes:
        nodes[node_name] = {}
    nodes[node_name]["verify"] = verify
