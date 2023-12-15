from collections import deque

from app.behaviors.routes.route import Route


class Beam(Route):
    def __init__(self, graph, root, destiny, priority, heuristic):
        super().__init__(graph, root, destiny, priority, heuristic)
        self.levelQueue = deque()
        self.beamWidth = 2

    def search(self):
        level = 0
        beam = [(0, self.root, ())]
        goal = False
        while not goal:
            newBeam = []
            print('***** *****')
            print(f'beam: {beam}')
            for beamItem in beam:
                heuristicV = beamItem[0]
                grid = beamItem[1]
                posV = grid[0]
                previousV = beamItem[2]

                if posV == self.destiny[0]:
                    self.auxList.append([posV, previousV, int(heuristicV)])
                    goal = True
                    break

                if posV not in self.visited:
                    self.visited.add(posV)
                    self.auxList.append([posV, previousV, int(heuristicV)])
                    adjList = self.graph[grid]
                    order = self.priority.priorityOrder(adjList)
                    print('----------')
                    print(f'posV: {posV}')
                    for prio in order:
                        posN = prio[0]
                        movN = prio[1]
                        typeN = prio[2]
                        codeN = prio[3]
                        if posN not in self.visited:
                            if self.root[1] == 'Robot' and typeN == 'Box' and posN != self.destiny[0]:
                                continue
                            else:
                                for heuN in self.heuristic[posN]:
                                    if heuN[1] == self.destiny[0]:
                                        print(f'posN: {posN}')
                                        i = 0
                                        if movN == self.priority.second:
                                            i = 0.001
                                        elif movN == self.priority.third:
                                            i = 0.002
                                        elif movN == self.priority.fourth:
                                            i = 0.003

                                        newBeam.append((heuN[0] + i, (posN, typeN, codeN), posV))


            if newBeam:
                level += 1
                newBeam.sort(key=lambda x: x[0], reverse=False)
                beam = newBeam[:self.beamWidth]
                if len(newBeam) > self.beamWidth:
                    auxBeam = newBeam[self.beamWidth: len(newBeam)]
                    self.levelQueue.append((level, auxBeam))
            else:
                aux = self.levelQueue.popleft()
                auxLevel = aux[0]
                auxBeam = aux[1]

                beam = auxBeam[:self.beamWidth]
                if len(auxBeam) > self.beamWidth:
                    self.levelQueue.append((auxLevel, auxBeam[self.beamWidth: len(auxBeam)]))
                    level = auxLevel


        return self.auxList
