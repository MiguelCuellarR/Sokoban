from queue import PriorityQueue

from app.behaviors.routes.route import Route
from resources.constants import valueStep


class UniformCost(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.queue = PriorityQueue()
        self.previousPos = ()

    def search(self):
        self.queue.put((0.0, self.root, ()))
        i = 0.00
        while self.queue:
            vertex = self.queue.get()
            routeSum = vertex[0]
            vertData = vertex[1]
            posV = vertData[0]
            typeV = vertData[1]
            codeV = vertData[2]
            previousV = vertex[2]

            if vertData == self.destiny:
                self.auxList.append([posV, previousV, int(routeSum)])
                break

            if posV not in self.visited:
                self.visited.add(posV)
                self.auxList.append([posV, previousV, int(routeSum)])
                adjList = self.graph[vertData]
                order = self.priority.priorityOrder(adjList)
                j = 0.000
                for prio in order:
                    posN = prio[0]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        summation = routeSum + valueStep
                        self.queue.put((summation + i + j, (posN, typeN, codeN), posV))
                        j = j + 0.001

                i = i + 0.01

        return self.auxList

    def buildPath(self):
        end = self.destiny[0]
        for step in reversed(self.auxList):
            if end == step[0] and end != self.root[0]:
                self.road.insert(0, step[0])
                end = step[1]

        return self.road