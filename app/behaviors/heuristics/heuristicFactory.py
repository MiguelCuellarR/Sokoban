from app.behaviors.heuristics.euclidian import Euclidian
from app.behaviors.heuristics.manhattan import Manhattan


class HeuristicFactory:

    @staticmethod
    def createHeuristic(typeRoute, ways, goals):
        heuristic = None
        if typeRoute == "Euclidian":
            heuristic = Euclidian(ways, goals)
        elif typeRoute == "Manhattan":
            heuristic = Manhattan(ways, goals)

        return heuristic.calculate()
