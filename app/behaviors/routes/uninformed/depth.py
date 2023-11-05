from collections import deque

from app.behaviors.routes.route import Route


class Depth(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.stack = deque()

    def search(self):
        self.stack.append(self.root)
        while self.stack:
            vertex = self.stack.pop()
            posV = vertex[0]
            typeV = vertex[1]
            codeV = vertex[2]

            if vertex == self.destiny:
                break


            if vertex not in self.visited:
                self.visited.add(posV)
                adjList = self.graph[vertex]

                order = self.priority.priorityOrder(adjList)

                for prio in reversed(order):
                    posN = prio[0]

                    if posN not in self.visited:
                        self.stack.append((prio[0], prio[2], prio[3]))
                        self.auxList.append([posV, posN])

        return self.auxList


    def buildPath(self):
        auxRoad = []
        end = self.destiny[0]
        for step in reversed(self.auxList):
            if end == step[1]:
                auxRoad.append(end)
                end = step[0]

            if end == self.root[0]:
                auxRoad.append(end)

        for step in reversed(auxRoad):
            self.road.append(step)

        return self.road
