import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from app.file.file import File
from app.agents.box import Box
from app.agents.goal import Goal
from app.agents.robot import Robot
from app.model.model import SokobanModel
from app.agents.wall import Wall
from app.agents.expansionOrder import ExpansionOrder

routes = [" ", "Beam", "Breadth", "ClimbHill"]
heuristics = [" ", "Euclidian"]

file = File()
world = file.uploadMap()
COLUMNS = len(world[0])
ROWS = len(world)

SIZE_OF_CANVAS_IN_PIXELS_X = 0
SIZE_OF_CANVAS_IN_PIXELS_Y = 0
if COLUMNS >= 7:
    SIZE_OF_CANVAS_IN_PIXELS_X = 750
else:
    SIZE_OF_CANVAS_IN_PIXELS_X = 400

if ROWS >= 5:
    SIZE_OF_CANVAS_IN_PIXELS_Y = 455
else:
    SIZE_OF_CANVAS_IN_PIXELS_Y = 400

simulation_params = {
    "routes": mesa.visualization.Choice(name="Selected Route", value=" ", choices=routes),
    "heuristics": mesa.visualization.Choice(name="Selected Heuristics", value=" ", choices=heuristics),
    "left": mesa.visualization.Slider(name='Left', value=0, min_value=0, max_value=4, step=1,
                                      description="Select a priority for left movement"),
    "up": mesa.visualization.Slider(name='Up', value=0, min_value=0, max_value=4, step=1,
                                    description="Select a priority for up movement"),
    "right": mesa.visualization.Slider(name='Right', value=0, min_value=0, max_value=4, step=1,
                                       description="Select a priority for right movement"),
    "down": mesa.visualization.Slider(name='Down', value=0, min_value=0, max_value=4, step=1,
                                      description="Select a priority for down movement"),
    "width": COLUMNS,
    "height": ROWS
}


def agent_portrayal(agent):
    portrayal = {"Shape": "resources/icons/floor1.png", "Layer": 0}
    if isinstance(agent, Wall):
        return {"Shape": "resources/icons/muro.png", "Layer": 0}
    elif isinstance(agent, ExpansionOrder):
        return {"Shape": agent.image, "Layer": 2}
    elif isinstance(agent, Robot):
        return {"Shape": "resources/icons/robot.png", "Layer": 3}
    elif isinstance(agent, Goal):
        return {"Shape": "resources/icons/bandera.png", "Layer": 1}
    elif isinstance(agent, Box):
        return {"Shape": "resources/icons/paquete.png", "Layer": 3}
    return portrayal


grid = CanvasGrid(agent_portrayal, COLUMNS, ROWS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)

server = ModularServer(SokobanModel, [grid], "Sokoban",
                       model_params=simulation_params)
server.port = 8521
server.launch()
