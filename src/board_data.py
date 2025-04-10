from typing import Tuple
from item_type import ItemType
from utility import Utility


class Item:
    def __init__(self, type):
        self.type: ItemType = type      # mező tartalma
        self.arrive_time: dict = {}     # kulcs id kigyo ennyi kör alatt érhet erre a mezőre


class Bodypart(Item):
    def __init__(self, type):
        super().__init__(type)
        self.id: str = ""              # kigyo id
        self.direction: str = ""       # testrész iránya mögötte lévő testrész alapján
        self.health: int = 100         # kigyo élet
        self.disappear_time: int = 1   # testrész eltűnési ideje
        self.length: int = 1           # kigyo hossza


class BoardData:
    def __init__(self, game_state, modename):
        self.board: list[list[Item]] = [
            [Item(ItemType.CLEAR) for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.height: int = game_state["height"]
        self.width: int = game_state["width"]
        self.modename: str = modename

        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                item = Item(ItemType.CLEAR)
                self.board[i].append(item)

    def refresh(self, game_state):
        self.clear_board()
        self.place_food(game_state["food"])
        self.place_hazards(game_state["hazards"])
        self.place_snakes(game_state["snakes"])
        self.calculate_arrival_times(game_state["snakes"])

    def clear_board(self):
        # üresítés
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = Item(ItemType.CLEAR)

    def place_food(self, food_list):
        # kaja
        for food in food_list:
            y = food["y"]
            x = food["x"]
            self.board[y][x].type = ItemType.FOOD

    def place_hazards(self, hazards):
        # veszély
        for hazard in hazards:
            y = hazard["y"]
            x = hazard["x"]
            self.board[y][x].type = ItemType.HAZARD

    def place_snakes(self, snakes):
        # kigyajok
        for snake in snakes:
            last_y: int = None
            last_x: int = None
            part_number = 0

            # kigyaj testrészek
            for bodypart in snake["body"]:
                y = bodypart["y"]
                x = bodypart["x"]

                # testrész objektum, ez kerül a boardba
                bodypartitem = Bodypart(ItemType.BODY)

                # fej
                if bodypart == snake["head"]:
                    bodypartitem.type = ItemType.HEAD
                    self.board[y][x].direction = "up"

                # farok
                elif bodypart == snake["body"][len(snake["body"]) - 1]:
                    bodypartitem.type = ItemType.TAIL
                    self.board[last_y][last_x].direction = Utility.get_direction(y, x, last_y, last_x)

                # amúgy test
                else:
                    bodypartitem.type = ItemType.BODY
                    self.board[last_y][last_x].direction = Utility.get_direction(y, x, last_y, last_x)

                # disappear_time megállapítás
                bodypartitem.disappear_time = snake["length"] - part_number

                # egyáb attribútumok
                bodypartitem.id = snake["id"]
                bodypartitem.health = snake["health"]
                bodypartitem.length = snake["length"]

                # temp változók
                part_number += 1
                last_y = y
                last_x = x

                self.board[y][x] = bodypartitem

    def calculate_arrival_times(self, snakes):
        # arrive_time megállapítása minden snakenek
        for snake in snakes:
            self.arrive_time_calculator(snake["head"]["x"], snake["head"]["y"], snake["id"], 1)

    # DFS graph traversal
    # TODO: BFS might be better
    def arrive_time_calculator(self, x, y, id, number):
        for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
            if self.modename == "wrapped":  # wrapped change
                i, j = Utility.wrapped_coords(i, j, self.width, self.height)
            if 0 <= i < self.width and 0 <= j < self.height:
                if self.board[j][i].type in ["clear", "food", "hazard"]:
                    if id not in self.board[j][i].arrive_time or self.board[j][i].arrive_time[id] > number:
                        self.board[j][i].arrive_time[id] = number
                        self.arrive_time_calculator(i, j, id, number + 1)
