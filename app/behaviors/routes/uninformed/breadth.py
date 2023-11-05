from collections import deque

from app.behaviors.routes.route import Route


class Breadth(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.queue = deque()

    def search(self):
        self.queue.append(self.root)
        while self.queue:
            vertex = self.queue.popleft()
            posV = vertex[0]
            typeV = vertex[1]
            codeV = vertex[2]

            if vertex == self.destiny:
                break

            if vertex not in self.visited:
                self.visited.add(posV)
                adjList = self.graph[vertex]

                order = self.priority.priorityOrder(adjList)
                for prio in order:
                    posN = prio[0]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        self.queue.append((posN, typeN, codeN))
                        self.auxList.append([posV, posN])

        return self.auxList

    def buildPath(self):
        end = self.destiny[0]
        for step in reversed(self.auxList):
            if end == step[1]:
                self.road.insert(0, end)
                end = step[0]

        return self.road
