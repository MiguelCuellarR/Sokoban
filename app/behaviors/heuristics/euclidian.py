from numpy import sqrt
from app.behaviors.heuristics.heuristic import Heuristic
from app.generalFunctions.generalFunction import createObject
from resources.constants import valueStep


class Euclidian(Heuristic):
    def __init__(self, ways, goals):
        super().__init__(ways, goals)

    def calculate(self):
        heuristicList = []
        for way in self.ways:
            values = []
            for goal in self.goals:
                x = abs(way[0][0] - goal[0][0])
                y = abs(way[0][1] - goal[0][1])
                value = valueStep * sqrt((x * x) + (y * y))
                values.append((value, goal[0]))

            heuristicList.append([way[0], values])

        self.objHeuristic = createObject(heuristicList)
        return self.objHeuristic
