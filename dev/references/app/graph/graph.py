from graph_building import graph


class OriginDB:
    def __init__(self) -> None:
        self.origins = {}

    def save_origin(self, id, origin):
        self.origins[id] = origin

    def get_origin(self, id):
        if id in self.origins:
            return self.origins[id]
        return None


def run(id, input, origins):
    state = {}
    state = {"input": input, "origin": origins.get_origin(id)}
    answer = graph.invoke(state)
    origins.save_origin(id, answer["origin"])
    return {"answer": answer["answers"][0], "buttons": answer["buttons"]}


# if __name__ == "__main__":
#     id = "test"
#     origins = OriginDB()
#     input = "далее"
#     print(run(id, "/start", origins))
#     print(run(id, "далее", origins))
#     print(run(id, "Чатбот", origins))
#     print(run(id, "Отлично!", origins))
#     print(run(id, "798", origins))
#     print(run(id, "пишёв нахой", origins))
