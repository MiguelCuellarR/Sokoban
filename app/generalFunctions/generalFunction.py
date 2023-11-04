from app.agents.wall import Wall


def createMapObject(mapModel):
    objectMap = {}
    for position in mapModel:
        objectMap[position[0]] = position[1]

    return objectMap
