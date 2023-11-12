from app.agents.wall import Wall


def createObject(mapList):
    objectMap = {}
    for position in mapList:
        objectMap[position[0]] = position[1]
    return objectMap
