class File:

    def uploadMap(self) -> list[list[str]]:
        map_data = []
        with open('resources/worlds/world.txt') as txt_file:
            for line in txt_file:
                char = line.strip().replace(',', '').replace('\t', '')
                char = char.split()
                map_data.append(char)
        return map_data

    def saveMap(self) -> str:
        pass

File.uploadMap(self=None)