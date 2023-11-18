import os

import cv2
import numpy as np


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


def imagesPng():
    dirPath = 'C:/Users/james/OneDrive/Escritorio/Sistemas inteligentes I/Proyecto/Sokoban/resources/numbers'
    for i in range(10, 101):
        cad = str(i)
        listDig = []
        for j in range(0, len(cad)):
            listDig.append(cad[j])
        imgComp = cv2.imread(dirPath + listDig[0] + '.png', cv2.IMREAD_UNCHANGED)
        for dig in listDig[1:]:
            img = cv2.imread(dirPath + dig + '.png', cv2.IMREAD_UNCHANGED)
            imgComp = cv2.hconcat((imgComp, img))
        resize = cv2.resize(imgComp, (512, 512))
        print(cad + '.png')
        cv2.imwrite(dirPath + cad + '.png', resize)

# imagesPng()
