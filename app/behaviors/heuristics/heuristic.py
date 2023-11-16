from abc import ABC


class Heuristic(ABC):
    def __init__(self, ways, goals):
        self.ways = ways
        self.goals = goals
        self.objHeuristic = {}

    def calculate(self):
        pass


