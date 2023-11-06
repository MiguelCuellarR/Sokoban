from collections import deque

from app.behaviors.routes.route import Route


class ClimbHill(Route):
    def __init__(self, graph, root, destiny, priority, heuristic):
        super().__init__(graph, root, destiny, priority, heuristic)
        self.levelQueue = deque()
        self.previousPos = ()

    def search(self):
        level = 0
        vertex = [0, self.root, ()]

        while vertex:
            routeSum = vertex[0]
            grid = vertex[1]
            posV = grid[0]
            typeV = grid[1]
            codeV = grid[2]
            previousV = vertex[2]

            break

        #self.levelQueue.put((self.heuristic[self.root[0]], [0, self.root, ()]))