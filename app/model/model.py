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


class SokobanModel(Model):

    def __init__(self, agentsAmount, width, height):
        world = File.uploadMap(self=None)
        self.agentsAmount = agentsAmount
        width = len(world[0])
        height = len(world)
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.datacollector = mesa.DataCollector(
            model_reporters={
            }
        )

        x = 0
        for i in range(width):
            for j in range(height):
                field = world[j][i]
                print(field)
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
                    robot = Robot(x, self)
                    self.grid.place_agent(robot, (i, j))
                    self.schedule.add(robot)

                if field[0:4] == "C-b-":
                    x = x + 1
                    road = Road(x, self)
                    self.grid.place_agent(road, (i, j))
                    self.schedule.add(road)

                    x = x + 1
                    box = Box(x, self)
                    self.grid.place_agent(box, (i, j))
                    self.schedule.add(box)
                x = x + 1

    def step(self) -> None:
        self.schedule.step()
        # Este permite actualizar los datos cada paso
        self.datacollector.collect(self)
