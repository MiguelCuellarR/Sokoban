from collections import deque

from app.behaviors.routes.route import Route


class Depth(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.stack = deque()

    def search(self):
        self.stack.append((self.root, ()))

        while self.stack:
            vertex = self.stack.pop()
            vertData = vertex[0]
            posV = vertData[0]
            typeV = vertData[1]
            codeV = vertData[2]
            previousV = vertex[1]

            if vertData == self.destiny:
                self.auxList.append([posV, previousV, ()])
                break

            if posV not in self.visited:
                self.visited.add(posV)
                self.auxList.append([posV, previousV, ()])
                adjList = self.graph[vertData]
                order = self.priority.priorityOrder(adjList)
                for prio in reversed(order):
                    posN = prio[0]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        self.stack.append(((posN, typeN, codeN), posV))

        return self.auxList

    def buildPath(self):
        end = self.destiny[0]
        for step in reversed(self.auxList):
            if end == step[0] and end != self.root[0]:
                self.road.insert(0, step[0])
                end = step[1]

        return self.road


