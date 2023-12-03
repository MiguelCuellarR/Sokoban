from collections import deque

from app.behaviors.routes.route import Route


class Breadth(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.queue = deque()

    def search(self):
        self.queue.append((self.root, ()))

        while self.queue:
            vertex = self.queue.popleft()
            posV = vertex[0][0]
            previousV = vertex[1]

            if vertex[0] == self.destiny:
                self.auxList.append([posV, previousV])
                break

            if posV not in self.visited:
                self.visited.add(posV)
                self.auxList.append([posV, previousV])

                adjList = self.graph[vertex[0]]
                order = self.priority.priorityOrder(adjList)

                for prio in order:
                    posN = prio[0]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        if self.root[1] == 'Robot' and typeN == 'Box' and posN != self.destiny[0]:
                            continue
                        else:
                            self.queue.append(((posN, typeN, codeN), posV))

        return self.auxList
