import mesa
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from app.agents.box import Box
from app.file.file import File
from app.agents.goal import Goal
from app.agents.road import Road
from app.agents.robot import Robot
from app.agents.wall import Wall
from app.behaviors.heuristics.heuristicFactory import HeuristicFactory
from app.behaviors.priority.priority import Priority
from app.behaviors.routes.routeFactory import RouteFactory
from app.generalFunctions import generalFunction
from app.generalFunctions.generalFunction import createObject


class SokobanModel(Model):

    def __init__(self, routes, heuristics, left, up, right, down, width, height):

        file = File()
        self.world = file.uploadMap()
        self.heuristics = heuristics
        self.routes = routes
        self.left = left
        self.up = up
        self.down = down
        self.right = right
        self.width = len(self.world[0])
        self.height = len(self.world)
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.datacollector = mesa.DataCollector(
            model_reporters={
            }
        )
        self.mapConstructor()

        prio = generalFunction.getPriorities([['L', self.left], ['U', self.up], ['D', self.down], ['R', self.right]])
        if prio[1] and prio[2] and prio[3] and prio[4]:
            self.priority = Priority(prio[1][0], prio[2][0], prio[3][0], prio[4][0])
        else:
            self.priority = Priority()

        self.boxesAgents, self.robotsAgents = [], []

        objectMap, robots, boxes, goals, ways = self.mapNeighbors()

        heuristicGoal, heuristicBox = {}, {}
        if ways and goals:
            heuristicGoal = HeuristicFactory.createHeuristic(self.heuristics, ways, goals)

        if objectMap and boxes and robots and goals and self.priority:
            if self.routes in ['Depth', 'Breadth', 'UniformCost']:
                for box in boxes:
                    for goal in goals:
                        if box[2] == goal[2]:
                            expansionOrder, road = RouteFactory.createRoute(self.routes, objectMap, box, goal,
                                                                            self.priority, {})
                            agents = self.grid[box[0]]
                            agent = [agent for agent in agents if isinstance(agent, Box)]
                            agent[0].road.append(road)
                            self.boxesAgents.append(agent[0])

                    for robot in robots:
                        if box[2] == robot[2]:
                            boxAgent = self.boxesAgents[len(self.boxesAgents) - 1]
                            nextB = boxAgent.road[0][0]
                            currentB = boxAgent.pos
                            nextR = self.moveIdentify(currentB, nextB)

                            expansionOrder, road = RouteFactory.createRoute(self.routes, objectMap, robot,
                                                                            (nextR, box[1], box[2]),
                                                                            self.priority, {})
                            agents = self.grid[robot[0]]
                            agent = [agent for agent in agents if isinstance(agent, Robot)]
                            agent[0].road.append(road)
                            self.robotsAgents.append(agent[0])
            else:
                if heuristicGoal:
                    for box in boxes:
                        for goal in goals:
                            if box[2] == goal[2]:
                                expansionOrder, road = RouteFactory.createRoute(self.routes, objectMap, box, goal,
                                                                                self.priority, heuristicGoal)
                                agents = self.grid[box[0]]
                                agent = [agent for agent in agents if isinstance(agent, Box)]
                                agent[0].road.append(road)
                                self.boxesAgents.append(agent[0])

                        for robot in robots:
                            if box[2] == robot[2]:
                                boxAgent = self.boxesAgents[len(self.boxesAgents) - 1]
                                nextB = boxAgent.road[0][0]
                                currentB = boxAgent.pos
                                nextR = self.moveIdentify(currentB, nextB)
                                aim = (nextR, box[1], box[2])
                                if aim and boxes:
                                    heuristicBox = HeuristicFactory.createHeuristic(self.heuristics, ways, [aim])
                                expansionOrder, road = RouteFactory.createRoute(self.routes, objectMap, robot, aim,
                                                                                self.priority, heuristicBox)
                                agents = self.grid[robot[0]]
                                agent = [agent for agent in agents if isinstance(agent, Robot)]
                                agent[0].road.append(road)
                                self.robotsAgents.append(agent[0])

    def step(self) -> None:
        self.schedule.step()
        if self.boxesAgents:
            box = self.boxesAgents[0]
            if box.road[0]:
                self.block(box)



        '''def expansionOrder(self, currentStep):
        currentStep = self.schedule.steps
        if currentStep < len(self.expansionOrder):
            move = self.expansionOrder[currentStep]
            nextPos = move[0]
            imagePath = "resources/numbers/" + str(currentStep) + ".png"
            expOrd = ExpansionOrder(currentStep + 1000, self, imagePath)
            self.grid.place_agent(expOrd, nextPos)
            self.schedule.add(expOrd)'''

    def block(self, box):
        square = self.grid[box.road[0][0]]

        if len(square) > 1:
            for neighbor in square:
                if isinstance(neighbor, Robot):
                    robotNeighbors = self.identifyPossiblePush(neighbor)
                    movement = self.selectMovement(robotNeighbors, neighbor)
                    self.grid.move_agent(neighbor, movement[1])

                elif isinstance(neighbor, Goal):
                    self.robotPush(box)
                    break

                elif isinstance(neighbor, Box):
                    robot = next((robot for robot in self.robotsAgents if robot.code == neighbor.code), None)
                    boxNeighbors = self.identifyPossiblePush(neighbor)
                    movement = self.selectMovement(boxNeighbors, neighbor)
                    objectMap, _, _, _, ways = self.mapNeighbors()
                    aim = (movement[0], 'Box', neighbor.code)
                    heuristicBox = HeuristicFactory.createHeuristic(self.heuristics, ways, [aim])
                    _, road = RouteFactory.createRoute(self.routes, objectMap, (robot.pos, 'Robot',
                                                                                robot.code), aim,
                                                       self.priority, heuristicBox)
                    if len(neighbor.road[0]) > 1:
                        if neighbor.road[0][0] != movement[1] and neighbor.road[0][0] != neighbor.pos:
                            neighbor.road[0].insert(0, neighbor.pos)
                            neighbor.road[0].insert(0, movement[1])
                    robot.road[0] = road
                    self.robotPush(neighbor)
        else:
            self.robotPush(box)

    def robotPush(self, box):
        for robot in self.robotsAgents:
            if robot.code == box.code:
                if len(robot.road[0]) > 0:
                    self.grid.move_agent(robot, robot.road[0][0])
                    robot.road[0] = robot.road[0][1:]
                else:
                    nextPosBox = box.road[0][0]
                    self.grid.move_agent(robot, box.pos)
                    self.grid.move_agent(box, nextPosBox)
                    if len(box.road[0]) > 1:
                        box.road[0] = box.road[0][1:]
                        objectMap, _, _, _, ways = self.mapNeighbors()
                        nextR = self.moveIdentify(nextPosBox, box.road[0][0])
                        aim = (nextR, 'Box', box.code)
                        heuristicBox = HeuristicFactory.createHeuristic(self.heuristics, ways, [aim])
                        _, road = RouteFactory.createRoute(self.routes, objectMap, (robot.pos, 'Robot',
                                                                                    robot.code), aim,
                                                           self.priority, heuristicBox)
                        robot.road[0] = road
                    else:
                        self.boxesAgents = self.boxesAgents[1:]

    def identifyPossiblePush(self, neighbor):
        boxNeighbors = self.grid.get_neighbors(neighbor.pos, False)
        boxNeighbors = self.neighborIdentify(boxNeighbors, neighbor.pos[0], neighbor.pos[1])

        newBoxNeighbors = []
        for boxN in boxNeighbors:
            if boxN[1] == 'Box':
                if boxN[0][0] == 0 or boxN[0][0] == self.height - 1:
                    continue

                elif boxN[0][1] == 0 or boxN[0][1] == self.width - 1:
                    continue

            agents = self.grid[boxN[0]]
            possible = True
            for agent in agents:
                if isinstance(agent, Box) or isinstance(agent, Wall):
                    possible = False
            if not possible:
                continue
            else:
                newBoxNeighbors.append(boxN)
        return newBoxNeighbors

    def selectMovement(self, newBoxNeighbors, neighbor):
        movements = ()
        for newBoxNeighbors in newBoxNeighbors:
            newRPos = self.moveIdentify(neighbor.pos, newBoxNeighbors[0])
            agents = self.grid[newRPos]
            if isinstance(neighbor, Box):
                if len(agents) > 1:
                    agent = next(
                        (agent for agent in agents if isinstance(agent, Box)), None)
                    if agent:
                        continue
                    else:
                        movements = (newRPos, newBoxNeighbors[0])
                else:
                    if isinstance(agents[0], Wall):
                        continue
                    movements = (newRPos, newBoxNeighbors[0])
            else:
                return newRPos, newBoxNeighbors[0]

        return movements


    def mapConstructor(self):
        x = 0
        for i in range(self.width):
            for j in range(self.height):
                field = self.world[j][i]
                if field[0] == "M":
                    x = x + 1
                    road = Road(x, self)
                    self.grid.place_agent(road, (i, j))
                    self.schedule.add(road)

                    x = x + 1
                    goal = Goal(x, self, field[len(field) - 1])
                    self.grid.place_agent(goal, (i, j))
                    self.schedule.add(goal)

                if field == "C":
                    road = Road(x, self)
                    self.grid.place_agent(road, (i, j))
                    self.schedule.add(road)

                if field == "R":
                    wall = Wall(x, self)
                    self.grid.place_agent(wall, (i, j))
                    self.schedule.add(wall)

                if field[0:3] == "C-a":
                    x = x + 1
                    road = Road(x, self)
                    self.grid.place_agent(road, (i, j))
                    self.schedule.add(road)

                    x = x + 1
                    robot = Robot(x, self, field[len(field) - 1])
                    self.grid.place_agent(robot, (i, j))
                    self.schedule.add(robot)

                if field[0:3] == "C-b":
                    x = x + 1
                    road = Road(x, self)
                    self.grid.place_agent(road, (i, j))
                    self.schedule.add(road)

                    x = x + 1
                    box = Box(x, self, field[len(field) - 1])
                    self.grid.place_agent(box, (i, j))
                    self.schedule.add(box)
                x = x + 1

    def mapNeighbors(self):
        mapModel = []
        robots, boxes, goals, ways = [], [], [], []
        for i in range(self.width):
            for j in range(self.height):
                # i=Column, j=Row
                for agent in self.grid[i, j]:
                    if not isinstance(agent, Wall):
                        agentData, agentType = self.agentIdentify(agent)
                        if agentType == 'W':
                            ways.append(agentData)
                        elif agentType == 'R':
                            robots.append(agentData)
                        elif agentType == 'B':
                            boxes.append(agentData)
                        elif agentType == 'G':
                            goals.append(agentData)

                        neighbors = self.grid.get_neighbors(agentData[0], False)
                        neighborList = self.neighborIdentify(neighbors, i, j)
                        mapModel.append([agentData, neighborList])

        objectMap = createObject(mapModel)
        return objectMap, robots, boxes, goals, ways

    @staticmethod
    def agentIdentify(agent):
        agentType = ''
        agentPos = agent.pos
        agentName = agent.__class__.__name__
        code = 0

        if isinstance(agent, Robot):
            code = agent.code
            agentType = 'R'
        elif isinstance(agent, Box):
            code = agent.code
            agentType = 'B'
        elif isinstance(agent, Goal):
            code = agent.code
            agentType = 'G'
        elif isinstance(agent, Road):
            agentType = 'W'  # Way
        agentData = (agentPos, agentName, code)

        return agentData, agentType

    @staticmethod
    def neighborIdentify(neighbors, i, j):
        neighborList = []
        for neighbor in neighbors:
            neighborPos = neighbor.pos
            neighborName = neighbor.__class__.__name__
            code = 0

            if isinstance(neighbor, Box):
                code = neighbor.code
            elif isinstance(neighbor, Robot):
                code = neighbor.code
            elif isinstance(neighbor, Goal):
                code = neighbor.code

            # L, D, U, R
            if i - 1 == neighborPos[0]:
                neighborList.append([neighborPos, 'L', neighborName, code])
            elif j - 1 == neighborPos[1]:
                neighborList.append([neighborPos, 'D', neighborName, code])
            elif j + 1 == neighborPos[1]:
                neighborList.append([neighborPos, 'U', neighborName, code])
            elif i + 1 == neighborPos[0]:
                neighborList.append([neighborPos, 'R', neighborName, code])

        return neighborList

    @staticmethod
    def moveIdentify(current, nextP):
        if current[0] > nextP[0]:
            return current[0] + 1, current[1]
        elif current[0] < nextP[0]:
            return current[0] - 1, current[1]
        elif current[1] > nextP[1]:
            return current[0], current[1] + 1
        elif current[1] < nextP[1]:
            return current[0], current[1] - 1
