from typing import List


class File():

    def uploadMap(self) -> list[list[str]]:
        map_data = []
        with open("mundo.txt") as txt_file:
            for line in txt_file:
                map_data.append(line.strip().split())
        return map_data

    def saveMap(self) -> str:
        pass
