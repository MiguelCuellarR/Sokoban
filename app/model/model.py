import mesa
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from app.agents.box import Box
from app.agents.expansionOrder import ExpansionOrder
from app.agents.goal import Goal
from app.agents.road import Road
from app.agents.robot import Robot
from app.agents.wall import Wall
from app.behaviors.heuristics.heuristicFactory import HeuristicFactory
from app.behaviors.priority.priority import Priority
from app.behaviors.routes.routeFactory import RouteFactory
from app.file.file import File
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

        priority = generalFunction.getPriorities([['L', self.left], ['U', self.up], ['D', self.down], ['R', self.right]])
        if priority[1] and priority[2] and priority[3] and priority[4]:
            priority = Priority(priority[1][0], priority[2][0], priority[3][0], priority[4][0])
        else:
            priority = Priority()

        objectMap, robots, boxes, goals, ways = self.mapNeighbors()
        heuristic = {}
        if ways and goals:
            heuristic = HeuristicFactory.createHeuristic(self.heuristics, ways, goals)

        if objectMap and robots and goals and priority:
            if self.routes in ['Depth', 'Breadth', 'UniformCost']:
                self.expansionOrder, self.road = RouteFactory.createRoute(self.routes, objectMap, robots[0], goals[0],
                                                                          priority, {})
            else:
                if heuristic:
                    self.expansionOrder, self.road = RouteFactory.createRoute(self.routes, objectMap, robots[0],
                                                                              goals[0], priority, heuristic)
            #self.expansionOrder, self.road = RouteFactory.createRoute(self.routes, objectMap, robots[0], goals[1],
            # priority, heuristic)

    def step(self) -> None:
        self.schedule.step()
        currentStep = self.schedule.steps
        if currentStep < len(self.expansionOrder):
            move = self.expansionOrder[currentStep]
            nextPos = move[0]
            imagePath = "resources/numbers/" + str(currentStep) + ".png"
            expOrd = ExpansionOrder(currentStep + 1000, self, imagePath)
            self.grid.place_agent(expOrd, nextPos)
            self.schedule.add(expOrd)

        #self.datacollector.collect(self)

    def mapConstructor(self):
        x = 0
        for i in range(self.width):
            for j in range(self.height):
                field = self.world[j][i]
                if field == "M":
                    x = x + 1
                    road = Road(x, self)
                    self.grid.place_agent(road, (i, j))
                    self.schedule.add(road)

                    x = x + 1
                    goal = Goal(x, self)
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
        agentData = ()
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
