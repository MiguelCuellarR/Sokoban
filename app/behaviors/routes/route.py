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

    def search(self):
        pass

    def buildPath(self):
        end = self.destiny[0]
        prev = self.previousPos
        for step in reversed(self.auxList):
            if end == step[2] and prev == step[1]:
                self.road.insert(0, step[2])
                end = step[1]
                prev = step[0]

        return self.road
