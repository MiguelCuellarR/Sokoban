from collections import deque

from app.behaviors.routes.route import Route


class Depth(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.stack = deque()
        self.previousPos = ()

    def search(self):
        self.stack.append((self.root, ()))

        while self.stack:
            vertex = self.stack.pop()
            posV = vertex[0][0]
            typeV = vertex[0][1]
            codeV = vertex[0][2]
            previousV = vertex[1]

            if vertex[0] == self.destiny:
                self.previousPos = previousV
                break

            if vertex not in self.visited:
                self.visited.add(posV)

                adjList = self.graph[vertex[0]]
                order = self.priority.priorityOrder(adjList)
                for prio in reversed(order):
                    posN = prio[0]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        self.stack.append(((posN, typeN, codeN), posV))
                        self.auxList.append([previousV, posV, posN])

        return self.auxList
