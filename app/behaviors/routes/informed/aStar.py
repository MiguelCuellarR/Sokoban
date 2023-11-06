from queue import PriorityQueue

from app.behaviors.routes.route import Route
from resources.constants import valueStep


class AStar(Route):
    def __init__(self, graph, root, destiny, priority, heuristic):
        super().__init__(graph, root, destiny, priority, heuristic)
        self.queue = PriorityQueue()
        self.previousPos = ()

    def search(self):
        self.queue.put((self.heuristic[self.root[0]], [0, self.root, ()]))

        while self.queue:
            vertex = self.queue.get()
            routeSum = vertex[1][0]
            grid = vertex[1][1]
            posV = grid[0]
            typeV = grid[1]
            codeV = grid[2]
            previousV = vertex[1][2]

            if grid == self.destiny:
                self.previousPos = previousV
                break

            auxHeuristics = vertex[0]

            for auxHeu in auxHeuristics:
                valueH = auxHeu[0]
                posH = auxHeu[1]

                if self.destiny[0] == posH:
                    if posV not in self.visited:
                        self.visited.add(posV)
                        adjList = self.graph[grid]
                        order = self.priority.priorityOrder(adjList)

                        for prio in order:
                            posN = prio[0]
                            typeN = prio[2]
                            codeN = prio[3]
                            if posN not in self.visited:
                                routeSum = routeSum + valueStep
                                f = valueH + routeSum
                                self.queue.put(([(f, posH)], [routeSum, (posN, typeN, codeN), posV]))
                                self.auxList.append([previousV, posV, posN, round(f, 2)])

        return self.auxList

    def buildPath(self):
        end = self.destiny[0]
        prev = self.previousPos
        for step in reversed(self.auxList):
            if end == step[2] and prev == step[1]:
                self.road.insert(0, step[2])
                end = step[1]
                prev = step[0]

        return self.road
