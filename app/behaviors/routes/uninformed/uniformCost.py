from queue import PriorityQueue

from app.behaviors.routes.route import Route
from resources.constants import valueStep


class UniformCost(Route):
    def __init__(self, graph, root, destiny, priority):
        super().__init__(graph, root, destiny, priority)
        self.queue = PriorityQueue()
        self.previousPos = ()

    def search(self):
        vertex = (0, self.root, ())
        while vertex:
            routeSum = vertex[0]
            vertData = vertex[1]
            posV = vertData[0]
            typeV = vertData[1]
            codeV = vertData[2]
            previousV = vertex[2]

            if vertData == self.destiny:
                self.auxList.append([posV, previousV, int(routeSum)])
                break

            if posV not in self.visited:
                self.visited.add(posV)
                self.auxList.append([posV, previousV, int(routeSum)])
                adjList = self.graph[vertData]
                order = self.priority.priorityOrder(adjList)
                i = 0.000
                for prio in order:
                    posN = prio[0]
                    movN = prio[1]
                    typeN = prio[2]
                    codeN = prio[3]

                    if posN not in self.visited:
                        if movN == self.priority.second:
                            i = 0.001
                        elif movN == self.priority.third:
                            i = 0.002
                        elif movN == self.priority.fourth:
                            i = 0.003

                    summation = routeSum + valueStep
                    self.queue.put((summation + i, (posN, typeN, codeN), posV))
            vertex = self.queue.get()

        return self.auxList

    def _movePriority(self):
        vertex = self.queue.get()

        auxList = []
        while not self.queue.empty():
            auxV = self.queue.get()
            left, up, right, down = (), (), (), ()
            if vertex[0] == auxV[0]:
                vertexPosI = vertex[1][0][0]
                auxPosI = auxV[1][0][0]
                vertexPosJ = vertex[1][0][1]
                auxPosJ = auxV[1][0][1]

                if vertexPosI > auxPosI:
                    right = vertex
                    left = auxV
                elif vertexPosI < auxPosI:
                    right = auxV
                    left = vertex

                if vertexPosJ > auxPosJ:
                    up = vertex
                    down = auxV
                elif vertexPosJ < auxPosJ:
                    up = auxV
                    down = vertex

                decision = self._returnPriority(left, right, up, down)
                if decision:
                    name = decision[0]
                    vertex = decision[1]

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

        return vertex

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
