class File:

    def uploadMap(self) -> list[list[str]]:
        map_data = []
        with open('resources/worlds/world10.txt') as txt_file:
            for line in txt_file:
                char = line.strip().replace('\t', '').replace(',', ' ')
                char = char.split()
                map_data.append(char)
        map_data = reversed(map_data)

        map_model = []
        for model in map_data:
            map_model.append(model)
        return map_model

    def saveMap(self, data, i):
        with open('resources/states.txt', 'a') as file:
            file.write('Nodo ' + str(i) + '\n')
            for line in reversed(data):
                file.write(' '.join(line) + '\n')

            file.write('\n')

    def clearMap (self):
        with open('resources/states.txt', 'w') as file:
            file.truncate(0)
