from queue import PriorityQueue

from app.behaviors.routes.route import Route
from resources.constants import valueStep


class AStar(Route):
    def __init__(self, graph, root, destiny, priority, heuristic):
        super().__init__(graph, root, destiny, priority, heuristic)
        self.queue = PriorityQueue()
        self.previousPos = ()

    def search(self):
        heuristics = self.heuristic[self.root[0]]
        for heuristic in heuristics:
            self.queue.put((heuristic[0], heuristic[1], [0, self.root, ()]))

        while not self.queue.empty():
            square = self.queue.get()
            auxH = square[1]
            grid = square[2]
            routeSum = grid[0]
            posV = grid[1][0]
            typeV = grid[1][1]
            codeV = grid[1][2]
            previousV = grid[2]

            if grid[1] == self.destiny:
                self.auxList.append([posV, previousV, round(square[0], 2)])
                break

            if auxH == self.destiny[0] and posV not in self.visited:
                self.visited.add(posV)
                self.auxList.append([posV, previousV, round(square[0], 2)])

                adjList = self.graph[grid[1]]
                order = self.priority.priorityOrder(adjList)
                i = 0
                for prio in order:
                    posN = prio[0]
                    movN = prio[1]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        for heuN in self.heuristic[posN]:
                            if heuN[1] == self.destiny[0]:
                                if movN == self.priority.second:
                                    i = 0.01
                                elif movN == self.priority.third:
                                    i = 0.02
                                elif movN == self.priority.fourth:
                                    i = 0.03

                                valueH = heuN[0]
                                summation = routeSum + valueStep
                                f = summation + valueH
                                self.queue.put((f+i, auxH, [summation, (posN, typeN, codeN), posV]))
        return self.auxList
