from app.behaviors.routes.route import Route
from queue import PriorityQueue


class BeamSearch(Route):

    def __init__(self, graph, root, destiny, priority, heuristic):
        super().__init__(graph, root, destiny, priority, heuristic)
        self.queue = PriorityQueue()
        self.previousPos = ()

    def beamSearch(self):
        current_level = {self.root}
        next_level = set()
        beamWidth = 0
        visited = set()
        paths = {self.root: [self.root]}

        for coun in self.graph.values():
            if beamWidth < len(coun):
                beamWidth = len(coun)

        while current_level:
            for node in current_level:
                if node == self.destiny:
                    return paths[node]

                if node not in visited:
                    visited.add(node)

                    # Expandir el nodo y obtener sus hijos
                    new_childrens = self.childrens(self.graph, node, self.heuristic)

                    # Ordenar los hijos por heurística y tomar los mejores "beamWidth" hijos
                    new_childrens.sort(key=lambda x: x[1])
                    selected_childrens = new_childrens[:beamWidth]

                    # Actualizar la lista de nodos para el próximo nivel
                    next_level.update(child[0] for child in selected_childrens)

                    # Actualizar los caminos hacia los hijos
                    for child_node, _ in selected_childrens:
                        paths[child_node] = paths[node] + [child_node]

            current_level = next_level
            next_level = set()
        return []

    def childrens(self, graph, node, heuristic):
        sons = []
        for key, value in graph[node]:
            sons.append([key, heuristic.get(key)])
        return sons
