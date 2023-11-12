from collections import deque
from queue import PriorityQueue

from app.behaviors.routes.route import Route


class ClimbHill(Route):
    def __init__(self, graph, root, destiny, priority, heuristic):
        super().__init__(graph, root, destiny, priority, heuristic)
        self.levelQueue = deque()
        self.previousPos = ()

    def search(self):
        level = 0
        vertex = (0, self.root, ())
        while vertex:
            heuristicV = vertex[0]
            grid = vertex[1]
            posV = grid[0]
            typeV = grid[1]
            codeV = grid[2]
            previousV = vertex[2]

            if grid == self.destiny:
                self.auxList.append([posV, previousV, int(heuristicV)])
                break

            if posV not in self.visited:
                queue = PriorityQueue()
                auxEdgeList = []
                self.visited.add(posV)
                self.auxList.append([posV, previousV, int(heuristicV)])
                adjList = self.graph[grid]
                order = self.priority.priorityOrder(adjList)

                for prio in order:
                    posN = prio[0]
                    movN = prio[1]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        for heuN in self.heuristic[posN]:
                            if heuN[1] == self.destiny[0]:
                                auxEdgeList.append([heuN[0], posN, movN, typeN, codeN])

                if auxEdgeList:
                    level += 1
                    for aux in auxEdgeList:
                        mov = aux[2]
                        i = 0
                        if mov == self.priority.second:
                            i = 0.01
                        elif mov == self.priority.third:
                            i = 0.02
                        elif mov == self.priority.fourth:
                            i = 0.03

                        queue.put((aux[0] + i, (aux[1], aux[3], aux[4]), posV))
                    vertex = queue.get()
                    self.levelQueue.append((level, queue))

                else:
                    aux = self.levelQueue.popleft()
                    auxLevel = aux[0]
                    queue = aux[1]
                    vertex = queue.get()
                    if not queue.empty():
                        self.levelQueue.appendleft((auxLevel, queue))

        return self.auxList
