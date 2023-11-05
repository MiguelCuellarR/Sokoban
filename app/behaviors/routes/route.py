from abc import ABC


class Route(ABC):
    def __init__(self, graph, root, destiny, priority, heuristic=None):
        self.graph = graph
        self.root = root
        self.destiny = destiny
        self.priority = priority
        self.visited = set()
        self.auxList = []
        self.road = []
        self.heuristic = heuristic

    def search(self):
        pass

    def buildPath(self):
        pass
