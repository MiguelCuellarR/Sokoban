from collections import deque

from app.behaviors.routes.route import Route


class Breadth(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.queue = deque()
        self.previousPos = ()

    def search(self):
        self.queue.append((self.root, ()))
        self.visited.add(self.root[0])
        while self.queue:
            vertex = self.queue.popleft()
            posV = vertex[0][0]
            typeV = vertex[0][1]
            codeV = vertex[0][2]
            previousV = vertex[1]

            if vertex[0] == self.destiny:
                self.previousPos = previousV
                break

            adjList = self.graph[vertex[0]]
            order = self.priority.priorityOrder(adjList)
            for prio in order:
                posN = prio[0]
                typeN = prio[2]
                codeN = prio[3]
                if posN not in self.visited:
                    self.visited.add(posN)
                    self.queue.append(((posN, typeN, codeN), posV))
                    self.auxList.append([posN, posV, previousV])

        return self.auxList


