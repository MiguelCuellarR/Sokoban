import mesa
from app.agents.box import Box
from app.agents.road import Road
from app.file.file import File
from app.agents.expansionOrder import ExpansionOrder
from app.agents.goal import Goal
from app.agents.robot import Robot
from app.agents.wall import Wall
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa import Model
from app.generalFunctions.generalFunction import createMapObject


class SokobanModel(Model):

    def __init__(self, agentsAmount, width, height):
        self.world = File.uploadMap(self=None)
        self.agentsAmount = agentsAmount
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

        objectMap = self.mapNeighbors()



    def step(self) -> None:
        self.schedule.step()
        # Este permite actualizar los datos cada paso
        self.datacollector.collect(self)


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
                    robot = Robot(x, self, field[len(field)-1])
                    self.grid.place_agent(robot, (i, j))
                    self.schedule.add(robot)

                if field[0:3] == "C-b":
                    x = x + 1
                    road = Road(x, self)
                    self.grid.place_agent(road, (i, j))
                    self.schedule.add(road)

                    x = x + 1
                    box = Box(x, self, field[len(field)-1])
                    self.grid.place_agent(box, (i, j))
                    self.schedule.add(box)
                x = x + 1


    def mapNeighbors(self):
        map = []
        boxes = []
        robots = []
        metas = []
        for i in range(self.width):
            for j in range(self.height):
                for agent in self.grid[i, j]:#i=Column, j=Row
                    if isinstance(agent, Box):
                        agentData = ((i, j), agent.__class__.__name__)
                        neighbors = self.grid.get_neighbors((i, j), False)
                        neighborList = []
                        for neighbor in neighbors:
                            pos = neighbor.pos
                            # L, D, U, R
                            if i-1 == pos[0]:
                                neighborList.append([pos, 'F', neighbor.__class__.__name__])
                            elif j-1 == pos[1]:
                                neighborList.append([pos, 'D', neighbor.__class__.__name__])
                            elif j+1 == pos[1]:
                                neighborList.append([pos, 'U', neighbor.__class__.__name__])
                            elif i+1 == pos[0]:
                                neighborList.append([pos, 'R', neighbor.__class__.__name__])
                        map.append([agentData, neighborList])

        objectMap = createMapObject(map)
        return objectMap