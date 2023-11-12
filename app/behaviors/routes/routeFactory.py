from app.behaviors.routes.informed.aStar import AStar
from app.behaviors.routes.informed.beam import Beam
from app.behaviors.routes.informed.climbHill import ClimbHill
from app.behaviors.routes.uninformed.breadth import Breadth
from app.behaviors.routes.uninformed.depth import Depth
from app.behaviors.routes.uninformed.uniformCost import UniformCost


class RouteFactory:

    @staticmethod
    def createRoute(typeRoute, graph, root, destiny, priority, heuristic):
        route = None
        if typeRoute == "Depth":
            route = Depth(graph, root, destiny, priority)
        elif typeRoute == "Breadth":
            route = Breadth(graph, root, destiny, priority)
        elif typeRoute == "UniformCost":
            route = UniformCost(graph, root, destiny, priority)
        elif typeRoute == "AStar":
            route = AStar(graph, root, destiny, priority, heuristic)
        elif typeRoute == "ClimbHill":
            route = ClimbHill(graph, root, destiny, priority, heuristic)
        elif typeRoute == "Beam":
            route = Beam(graph, root, destiny, priority, heuristic)

        expansionOrder = route.search()
        road = route.buildPath()
        return expansionOrder, road
