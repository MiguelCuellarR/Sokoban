from collections import deque

from app.behaviors.routes.route import Route


class ClimbHill(Route):
    def __init__(self, graph, root, destiny, priority, heuristic):
        super().__init__(graph, root, destiny, priority, heuristic)
        self.levelQueue = deque()
        self.previousPos = ()

    def search(self):
        level = 0

        #self.levelQueue.put((self.heuristic[self.root[0]], [0, self.root, ()]))