import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from app.File.file import File
from app.agents.box import Box
from app.agents.goal import Goal
from app.agents.robot import Robot
from app.model.model import SokobanModel
from app.agents.wall import Wall
from app.agents.expansionOrder import ExpansionOrder

routes = ["AStar", "ClimbHill", "Breadth", "Depth", "UniformCost"]
heuristics = ["Euclidian", "Manhanttan"]
moves = ["Left", "Right", "Up", "Down"]
file = File()
world = file.uploadMap()
COLUMNS = len(world[0])
ROWS = len(world)
SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {
    "routes": mesa.visualization.Choice(name="Selected Route", value="AStar", choices=routes),
    "heuristics": mesa.visualization.Choice(name="Selected Heuristics", value="Euclidian", choices=heuristics),
    "priority1": mesa.visualization.Choice(name="Selected moves", value="Left", choices=moves),
    "width": COLUMNS,
    "height": ROWS
}


def agent_portrayal(agent):
    portrayal = {"Shape": "resources/icons/pavimentacion.png", "Layer": 0}
    if isinstance(agent, Wall):
        return {"Shape": "resources/icons/muro.png", "Layer": 0}
    elif isinstance(agent, ExpansionOrder):
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": True, "Color": "#DFC49C", "text": "1", "text_color": "Black",
                "Layer": 2}
    elif isinstance(agent, Robot):
        return {"Shape": "resources/icons/robot.png", "Layer": 2}
    elif isinstance(agent, Goal):
        return {"Shape": "resources/icons/bandera.png", "Layer": 1}
    elif isinstance(agent, Box):
        return {"Shape": "resources/icons/paquete.png", "Layer": 2}
    return portrayal


grid = CanvasGrid(agent_portrayal, COLUMNS, ROWS, SIZE_OF_CANVAS_IN_PIXELS_X,
                  SIZE_OF_CANVAS_IN_PIXELS_Y)

chart_currents = ChartModule(
    [
        {"Label": "Wealthy Agents", "Color": "", "label": "Poder", "backgroundColor": "Blue"},
        {"Label": "Non Wealthy Agents", "Color": "", "label": "No Poder", "backgroundColor": "Red"},
    ],
    data_collector_name="datacollector"
)

server = ModularServer(SokobanModel, [grid, chart_currents], "Sokoban",
                       model_params=simulation_params)
server.port = 8521
server.launch()
