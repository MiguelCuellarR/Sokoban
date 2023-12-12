def createObject(mapList):
    objectMap = {}
    for position in mapList:
        objectMap[position[0]] = position[1]
    return objectMap


def getPriorities(movements):
    priorities = {}
    for mov, prio in movements:
        if prio in priorities:
            priorities[prio].append(mov)
        else:
            priorities[prio] = [mov]

    movements = [[], [], [], [], []]
    for key in priorities:
        moves = priorities[key]
        movements[key].append(moves[0])
    return movements