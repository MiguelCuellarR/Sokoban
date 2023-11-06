from queue import PriorityQueue

from app.behaviors.routes.route import Route
from resources.constants import valueStep


class UniformCost(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.queue = PriorityQueue()
        self.previousPos = ()

    def search(self):
        self.queue.put((0, self.root, ()))

        while self.queue:
            vertex = self.queue.get()
            routeSum = vertex[0]
            posV = vertex[1][0]
            typeV = vertex[1][1]
            codeV = vertex[1][2]
            previousV = vertex[2]

            if vertex[1] == self.destiny:
                self.previousPos = previousV
                break

            if posV not in self.visited:
                self.visited.add(posV)
                adjList = self.graph[vertex[1]]
                order = self.priority.priorityOrder(adjList)

                for prio in order:
                    posN = prio[0]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        summation = routeSum + valueStep
                        self.queue.put((summation, (posN, typeN, codeN), posV))
                        self.auxList.append([previousV, posV, posN, summation])

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
