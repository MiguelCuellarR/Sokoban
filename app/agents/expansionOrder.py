from mesa import Agent


class ExpansionOrder(Agent):

    def __init__(self, unique_id, model, image):
        super().__init__(unique_id, model)
        self.image = image
