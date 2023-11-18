class Priority:
    def __init__(self, first='L', second='U', third='R', fourth='D'):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth

    def priorityOrder(self, adjList):
        dictPriority = {
            'L': [],
            'D': [],
            'U': [],
            'R': []
        }

        for element in adjList:
            prio = element[1]
            dictPriority[prio].append(element)

        first = dictPriority[self.first]
        second = dictPriority[self.second]
        third = dictPriority[self.third]
        fourth = dictPriority[self.fourth]

        order = [first, second, third, fourth]

        possibleStep = self.verifyPosition(order)
        return possibleStep

    @staticmethod
    def verifyPosition(order):
        possibleStep = []

        for prio in order:
            if prio:
                if len(prio) > 1:
                    for element in prio:
                        if element[2] == 'Goal':
                            possibleStep.append(element)
                else:
                    if prio[0][2] != 'Wall':
                        possibleStep.append(prio[0])

        return possibleStep
