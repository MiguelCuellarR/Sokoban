from collections import deque

from app.behaviors.routes.route import Route


class Beam(Route):
    def __init__(self, graph, root, destiny, priority, heuristic):
        super().__init__(graph, root, destiny, priority, heuristic)
        self.levelQueue = deque()
        self.previousPos = ()
        self.beamWidth = 4

    def search(self):
        level = 0
        beam = [(0, self.root, ())]
        goal = False
        while not goal:
            newBeam = []
            for beamItem in beam:
                heuristicV = beamItem[0]
                grid = beamItem[1]
                posV = grid[0]
                typeV = grid[1]
                codeV = grid[2]
                previousV = beamItem[2]

                if grid == self.destiny:
                    self.auxList.append([posV, previousV, int(heuristicV)])
                    goal = True
                    break


                if posV not in self.visited:
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
                                    i = 0
                                    if movN == self.priority.second:
                                        i = 0.01
                                    elif movN == self.priority.third:
                                        i = 0.02
                                    elif movN == self.priority.fourth:
                                        i = 0.03

                                    newBeam.append((heuN[0] + i, (posN, typeN, codeN), posV))


            if newBeam:
                level += 1
                newBeam.sort(key=lambda x: x[0], reverse=False)
                #print(newBeam)
                beam = newBeam[:self.beamWidth]
                self.levelQueue.append((level, beam))
            else:
                break

        return self.auxList

    def buildPath(self):
        end = self.destiny[0]
        for step in reversed(self.auxList):
            if end == step[0] and end != self.root[0]:
                self.road.insert(0, step[0])
                end = step[1]

        return self.road
    