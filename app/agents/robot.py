from mesa import Agent


class Robot(Agent):

    def __init__(self, unique_id, model, code):
        super().__init__(unique_id, model)
        self.code = code
        self.road = []
