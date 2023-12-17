from mesa import Agent


class Box(Agent):

    def __init__(self, unique_id, model, code):
        super().__init__(unique_id, model)
        self.code = code
        self.road = []
        self.expansion = []
