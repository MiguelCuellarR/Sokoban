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
                i = 0.000
                for prio in order:
                    posN = prio[0]
                    movN = prio[1]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        if movN == self.priority.second:
                            i = 0.001
                        elif movN == self.priority.third:
                            i = 0.002
                        elif movN == self.priority.fourth:
                            i = 0.003

                        summation = routeSum + valueStep
                        self.queue.put((summation + i, (posN, typeN, codeN), posV))

        return self.auxList
