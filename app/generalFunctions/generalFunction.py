from app.agents.wall import Wall


def createMapObject(map):
    objectMap = {}
    for position in map:
        objectMap[position[0]] = position[1]

    return objectMap