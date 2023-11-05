from collections import deque

from app.behaviors.routes.route import Route


class Depth(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.stack = deque()

    def search(self):
        self.stack.append(self.root)
        previousPos = ()
        while self.stack:
            vertex = self.stack.pop()
            posV = vertex[0]
            typeV = vertex[1]
            codeV = vertex[2]

            if vertex == self.destiny:
                self.auxList.append([previousPos, posV])
                break

            if vertex not in self.visited:
                self.visited.add(posV)
                if previousPos != ():
                    self.auxList.append([previousPos, posV])
                previousPos = posV

                adjList = self.graph[vertex]
                order = self.priority.priorityOrder(adjList)
                for prio in reversed(order):
                    posN = prio[0]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        self.stack.append((posN, typeN, codeN))

        return self.auxList


    def buildPath(self):
        end = self.destiny[0]
        for step in reversed(self.auxList):
            if end == step[1]:
                self.road.insert(0, end)
                end = step[0]

        return self.road
