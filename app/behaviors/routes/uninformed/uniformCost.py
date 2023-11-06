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
        self.visited.add(self.root[0])
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

            adjList = self.graph[vertex[1]]
            order = self.priority.priorityOrder(adjList)
            i = 0
            for prio in order:
                posN = prio[0]
                typeN = prio[2]
                codeN = prio[3]
                if posN not in self.visited:
                    print(posV, '      ', order, '       ', posN)
                    self.visited.add(posN)
                    summation = routeSum + valueStep
                    self.queue.put((summation + i, (posN, typeN, codeN), posV))
                    self.auxList.append([previousV, posV, posN, summation])
                    i += 1

        return self.auxList