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
        self.previousPos = ()

    def buildPath(self):
        end = self.destiny[0]
        for step in reversed(self.auxList):
            if end == step[0] and end != self.root[0]:
                self.road.insert(0, step[0])
                end = step[1]
        return self.road



