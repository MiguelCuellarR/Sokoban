class File:

    def uploadMap(self) -> list[list[str]]:
        map_data = []
        with open('resources/worlds/world4.txt') as txt_file:
            for line in txt_file:
                char = line.strip().replace(',', '').replace('\t', '')
                char = char.split()
                map_data.append(char)

        map_data = reversed(map_data)

        map_model = []
        for model in map_data:
            map_model.append(model)

        return map_model

    def saveMap(self) -> str:
        pass