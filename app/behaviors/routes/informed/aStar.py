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

        square = self.queue.get()
        while square:
            valueHeuristic = square[0]

            auxH = square[1]
            grid = square[2]
            routeSum = grid[0]
            posV = grid[1][0]
            typeV = grid[1][1]
            codeV = grid[1][2]
            previousV = grid[2]

            if grid[1] == self.destiny:
                self.auxList.append([posV, previousV, round(float(valueHeuristic), 3)])
                break

            if auxH == self.destiny[0] and posV not in self.visited:
                self.visited.add(posV)
                self.auxList.append([posV, previousV, round(float(valueHeuristic), 3)])

                adjList = self.graph[grid[1]]
                order = self.priority.priorityOrder(adjList)
                for prio in order:
                    posN = prio[0]
                    typeN = prio[2]
                    codeN = prio[3]
                    if posN not in self.visited:
                        for heuN in self.heuristic[posN]:
                            if heuN[1] == self.destiny[0]:
                                valueH = heuN[0]
                                summation = routeSum + valueStep
                                f = summation + valueH
                                self.queue.put((f, auxH, [summation, (posN, typeN, codeN), posV]))

            square = self._movePriority()

        return self.auxList

    def _movePriority(self):
        square = self.queue.get()
        valueHeuristic = square[0]
        grid = square[2]
        auxList = []
        while not self.queue.empty():
            auxV = self.queue.get()
            auxHeu = auxV[0]
            auxGrid = auxV[2]
            left, up, right, down = (), (), (), ()
            if valueHeuristic == auxHeu:
                vertexPosI = grid[1][0][0]
                auxPosI = auxGrid[1][0][0]
                vertexPosJ = grid[1][0][1]
                auxPosJ = auxGrid[1][0][1]

                if vertexPosI > auxPosI:
                    right = square
                    left = auxV
                elif vertexPosI < auxPosI:
                    right = auxV
                    left = square

                if vertexPosJ > auxPosJ:
                    up = square
                    down = auxV
                elif vertexPosJ < auxPosJ:
                    up = auxV
                    down = square

                decision = self._returnPriority(left, right, up, down)
                if decision:
                    name = decision[0]
                    square = decision[1]

                    if name == 'L':
                        auxList.append(right)
                    elif name == 'U':
                        auxList.append(down)
                    elif name == 'R':
                        auxList.append(left)
                    elif name == 'D':
                        auxList.append(up)
            else:
                self.queue.put(auxV)
                break

        if auxList:
            for v in auxList:
                self.queue.put(v)

        return square

    def _returnPriority(self, left, right, up, down):
        if self.priority.first == 'L':
            if left:
                return ['L', left]
        elif self.priority.first == 'U':
            if up:
                return ['U', up]
        elif self.priority.first == 'R':
            if right:
                return ['R', right]
        elif self.priority.first == 'D':
            if down:
                return ['D', down]

        if self.priority.second == 'L':
            if left:
                return ['L', left]
        elif self.priority.second == 'U':
            if up:
                return ['U', up]
        elif self.priority.second == 'R':
            if right:
                return ['R', right]
        elif self.priority.second == 'D':
            if down:
                return ['D', down]

        if self.priority.third == 'L':
            if left:
                return ['L', left]
        elif self.priority.third == 'U':
            if up:
                return ['U', up]
        elif self.priority.third == 'R':
            if right:
                return ['R', right]
        elif self.priority.third == 'D':
            if down:
                return ['D', down]

        if self.priority.fourth == 'L':
            if left:
                return ['L', left]
        elif self.priority.fourth == 'U':
            if up:
                return ['U', up]
        elif self.priority.fourth == 'R':
            if right:
                return ['R', right]
        elif self.priority.fourth == 'D':
            if down:
                return ['D', down]
