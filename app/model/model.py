import mesa

from app.agents.box import Box
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
        self.agentsAmount = agentsAmount

        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.datacollector = mesa.DataCollector(
            model_reporters={
            }
        )

        wall = Wall(100, self)
        self.grid.place_agent(wall, (0, 0))
        self.schedule.add(wall)

        expansionOrder = ExpansionOrder(10, self)
        self.grid.place_agent(expansionOrder, (1, 1))
        self.schedule.add(expansionOrder)

        robot = Robot(20, self)
        self.grid.place_agent(robot, (0, 1))
        self.schedule.add(robot)

        box = Box(30, self)
        self.grid.place_agent(box, (2, 2))
        self.schedule.add(box)

        goal = Goal(40, self)
        self.grid.place_agent(goal, (2, 0))
        self.schedule.add(goal)

        def step(self) -> None:
            self.schedule.step()
            # Este permite actualizar los datos cada paso
            self.datacollector.collect(self)

