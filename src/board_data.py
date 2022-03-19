class Item:
    name: str           # mező tartalma
    arrive_time: dict   # kulcs id kigyo ennyi kör alatt érhet erre a mezőre

    def __init__(self, name):
        self.name = name
        self.arrive_time = {}


class Bodypart(Item):
    id: str         # kigyo id
    direction: str  # testrész iránya mögötte lévő testrész alapján
    health: int     # kigyo élet
    dis_time: int   # testrész eltűnési ideje
    length: int     # kigyo hossza

    def __init__(self, name):
        super().__init__(name)
        self.id = None
        self.direction = None
        self.health = 100
        self.dis_time = 1
        self.length = 1


class BoardData:
    board = []
    height: int
    width: int
    modename: str

    def __init__(self, board, modename):
        self.height = board["height"]
        self.width = board["width"]
        self.modename = modename

        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                item = Item("clear")
                self.board[i].append(item)

    def get_dir(self, y, x, lasty, lastx) -> str:
        if lastx > x:
            return "right"
        elif lastx < x:
            return "left"
        elif lasty > y:
            return "up"
        return "down"

    def refresh(self, board):
        # üresítés
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = Item("clear")
                # self.board[i][j].name = "clear"

        # kaja
        for food in board["food"]:
            y = food["y"]
            x = food["x"]
            self.board[y][x].name = "food"

        # veszély
        for hazard in board["hazards"]:
            y = hazard["y"]
            x = hazard["x"]
            self.board[y][x].name = "hazard"

        # kigyajok
        for snake in board["snakes"]:
            lasty: int = None
            lastx: int = None
            part_number = 0

            # kigyaj testrészek
            for bodypart in snake["body"]:
                y = bodypart["y"]
                x = bodypart["x"]

                # testrész objektum, ez kerül a boardba
                bodypartitem = Bodypart("body")

                # fej
                if bodypart == snake["head"]:
                    bodypartitem.name = "head"
                    self.board[y][x].direction = "up"

                # farok
                elif bodypart == snake["body"][len(snake["body"]) - 1]:
                    bodypartitem.name = "tail"
                    self.board[lasty][lastx].direction = self.get_dir(y, x, lasty, lastx)

                # amúgy test
                else:
                    bodypartitem.name = "body"
                    self.board[lasty][lastx].direction = self.get_dir(y, x, lasty, lastx)

                # dis_time megállapítás
                bodypartitem.dis_time = snake["length"] - part_number

                # egyáb attribútumok
                bodypartitem.id = snake["id"]
                bodypartitem.health = snake["health"]
                bodypartitem.length = snake["length"]

                # temp változók
                part_number += 1
                lasty = y
                lastx = x

                self.board[y][x] = bodypartitem

        # arrive_time megállapítása
        for snake in board["snakes"]:
            self.arrive_time_calculator(snake["head"]["x"], snake["head"]["y"], snake["id"], 1)

    def wrap_coord_replace(self, x: int, y: int):
        if x < 0:
            x = self.width - 1
        if y < 0:
            y = self.height - 1
        if x >= self.width:
            x = 0
        if y >= self.height:
            y = 0

    # wrapped, kimesz palyarol, tuloldalt kijossz------------------------------------------------------------------
    def arrive_time_calculator(self, x, y, id, number):

        for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
            if self.modename == "wrapped":  # wrapped change------
                if i < 0:
                    i = self.width - 1
                if j < 0:
                    j = self.height - 1
                if i >= self.width:
                    i = 0
                if j >= self.height:
                    j = 0
            if 0 <= i < self.width and 0 <= j < self.height:
                if self.board[j][i].name in ["clear", "food", "hazard"]:

                    if id not in self.board[j][i].arrive_time:
                        self.board[j][i].arrive_time[id] = number
                        self.arrive_time_calculator(i, j, id, number + 1)

                    elif self.board[j][i].arrive_time[id] > number:
                        self.board[j][i].arrive_time[id] = number
                        self.arrive_time_calculator(i, j, id, number + 1)
