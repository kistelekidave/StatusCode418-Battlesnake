import random
from typing import List, Dict

from board_data import BoardData


def distance(point1: dict, point2: dict) -> int:
    return abs(point1["x"] - point2["x"]) + abs(point1["y"] - point2["y"])


"""
def count_free_neighbours(board: BoardData, x: int, y: int) -> int:
    count = 0
    free_fields = ["clear", "food", "tail"]
    if x < board.width - 1:
        if board.board[y][x + 1].name in free_fields:
            count += 1

    if x > 0:
        if board.board[y][x - 1].name in free_fields:
            count += 1

    if y < board.height - 1:
        if board.board[y + 1][x].name in free_fields:
            count += 1

    if y > 0:
        if board.board[y - 1][x].name in free_fields:
            count += 1

    return count
"""


# iranok kivalogatasa avoid_obstacles fuggveny szamara
def help_avoid_snake(board: BoardData, dead_moves: List[str], hazard_moves: List[str], x: int, y: int, direction: str):
    if board.board[y][x].name in ["head", "body"]:
        dead_moves.append(direction)

    elif board.board[y][x].name == "tail":
        if board.board[y][x].health == 100:
            dead_moves.append(direction)

    elif board.board[y][x].name == "hazard":
        hazard_moves.append(direction)


# pimitiv akadáaly kerules
def avoid_obstacles(data: dict, board: BoardData, possible_moves: List[str], hazard_moves: List[str]) -> List[str]:
    x = data["you"]["head"]["x"]
    y = data["you"]["head"]["y"]

    # da walls
    if x == board.width - 1:
        possible_moves.remove("right")
    elif x == 0:
        possible_moves.remove("left")

    if y == board.height - 1:
        possible_moves.remove("up")
    elif y == 0:
        possible_moves.remove("down")

    # bodies and hazards
    dead_moves = []
    for [i, j, direction] in [[x + 1, y, "right"], [x - 1, y, "left"], [x, y + 1, "up"], [x, y - 1, "down"]]:
        if 0 <= i < board.width and 0 <= j < board.height:
            help_avoid_snake(board, dead_moves, hazard_moves, i, j, direction)

    for move in dead_moves:
        if len(possible_moves) > 1:
            if move in possible_moves:
                possible_moves.remove(move)
    """
    for move in hazard_moves:
        if len(possible_moves) > 1:
            if move in possible_moves:
                possible_moves.remove(move)
    """
    return possible_moves


"""
# buta kajakereses legvonalban
def find_food(data: dict, board: BoardData, possible_moves: List[str]) -> List[str]:
    if len(possible_moves) > 1:
        favorable_moves = [str]
        remove_move = ""

        # legközelebbi food objektum a pályán légvonalban
        dist = distance({"x": 0, "y": 0}, {"x": board.width, "y": board.height})
        coord: dict = None
        for food in data["board"]["food"]:
            temp_dist = distance(data["you"]["head"], food)
            if temp_dist < dist:
                dist = temp_dist
                coord = food

        # opcionális irány a legközelebbi kaja felé
        if coord is not None:
            if coord["x"] > data["you"]["head"]["x"]:
                favorable_moves.append("right")
                if coord["y"] == data["you"]["head"]["y"]:
                    remove_move = "left"

            elif coord["x"] < data["you"]["head"]["x"]:
                favorable_moves.append("left")
                if coord["y"] == data["you"]["head"]["y"]:
                    remove_move = "right"

            if coord["y"] > data["you"]["head"]["y"]:
                favorable_moves.append("up")
                if coord["x"] == data["you"]["head"]["x"]:
                    remove_move = "down"

            elif coord["y"] < data["you"]["head"]["y"]:
                favorable_moves.append("down")
                if coord["x"] == data["you"]["head"]["x"]:
                    remove_move = "up"

            # favorable és possible metszete lesz az eredmény
            segment = []
            for move in favorable_moves:
                if move in possible_moves:
                    segment.append(move)

            # de ha a metszet üres kivonluk az esetleges ellentétes irányt
            if len(segment) == 0:
                if remove_move in possible_moves:
                    possible_moves.remove(remove_move)
            else:
                possible_moves = segment

    return possible_moves
"""


def food_recursion(board: BoardData, been: List[List[int]], x: int, y: int, my_id: str):
    for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
        if 0 <= i < board.width and 0 <= j < board.height:
            if board.board[j][i].name in ["clear", "hazard", "food"]:
                if board.board[j][i].arrive_time[my_id] < board.board[y][x].arrive_time[my_id]:
                    if [j, i] not in been:
                        been.append([i, j])
                        food_recursion(board, been, i, j, my_id)


# okosabb kajakereses erkezesi ido alapjan, utvonaltervezessel
def find_food_better(data: Dict, board: BoardData, possible_moves: List[str]) -> List[str]:
    fx = -1
    fy = -1
    im_first = False
    # closest_to_enemy = True
    my_time = distance({"x": 0, "y": 0}, {"x": board.width, "y": board.height})

    hx = data["you"]["head"]["x"]
    hy = data["you"]["head"]["y"]

    for food in data["board"]["food"]:
        temp_my_time = -1
        temp_im_first = True
        # saját időm
        if data["you"]["id"] in board.board[food["y"]][food["x"]].arrive_time:
            temp_my_time = board.board[food["y"]][food["x"]].arrive_time[data["you"]["id"]]

        # egyátalán eljutok -e oda
        if temp_my_time != -1:
            # mások hamarabb érnek -e oda
            for key in board.board[food["y"]][food["x"]].arrive_time:
                if key != data["you"]["id"]:
                    if board.board[food["y"]][food["x"]].arrive_time[key] <= temp_my_time:
                        temp_im_first = False

            # én vagyok elso
            if temp_im_first:
                # eddig nem voltam első akkor frissül
                if not im_first:
                    fx = food["x"]
                    fy = food["y"]
                    im_first = True
                    my_time = temp_my_time

                # eddig is első voltam és jobb az időm akkor frissül
                elif my_time > temp_my_time:
                    fx = food["x"]
                    fy = food["y"]
                    im_first = True
                    my_time = temp_my_time

            # nem vagyok első
            elif my_time > temp_my_time:

                # eddig sem voltam elso és jobb az időm akkor frissül
                if not im_first:
                    fx = food["x"]
                    fy = food["y"]
                    my_time = temp_my_time

    been = []
    # utvonal a legjobbhoz
    if my_time != -1:
        been.append([fx, fy])
        food_recursion(board, been, fx, fy, data["you"]["id"])

    food_moves = []
    # iranyok szelektalasa
    for [i, j, direction] in [[hx + 1, hy, "right"], [hx - 1, hy, "left"], [hx, hy + 1, "up"], [hx, hy - 1, "down"]]:
        if [i, j] in been and direction in possible_moves:
            food_moves.append(direction)

    if len(food_moves) > 0:
        possible_moves = food_moves

    return possible_moves


def help_to_head(data: Dict, board: BoardData, x: int, y: int) -> list:
    can_go = True
    attack = False

    for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
        if 0 <= i < board.width and 0 <= j < board.height:
            if board.board[j][i].name == "head":
                if board.board[j][i].id != data["you"]["id"]:
                    if board.board[j][i].length >= data["you"]["length"]:
                        can_go = False
                    elif board.board[j][i].name != "hazard":
                        attack = True

    return [can_go, attack]


# fejeles tervezes szomszedos mezokon
# oda nem mehetsz ahova másik head el tud menni és nagyobb vagy egyenlő hosszú, CSAK HA MUSZÁLY
# oda mész ahova másik head tud menni és rövidebb
def who_to_head(data: Dict, board: BoardData, possible_moves: List[str]) -> List[str]:
    x = data["you"]["head"]["x"]
    y = data["you"]["head"]["y"]
    attack_moves = []
    if len(possible_moves) > 1:

        for [i, j, direction] in [[x + 1, y, "right"], [x - 1, y, "left"], [x, y + 1, "up"], [x, y - 1, "down"]]:
            if 0 <= i < board.width and 0 <= j < board.height:
                if board.board[j][i].name in ["clear", "food", "hazard"] or board.board[j][i].name == "tail" and board.board[j][i].dis_time == 1:
                    output = help_to_head(data, board, i, j)
                    if not output[0]:
                        if direction in possible_moves:
                            possible_moves.remove(direction)
                    elif output[1]:
                        if direction in possible_moves:
                            attack_moves.append(direction)

        if len(attack_moves) > 0:
            possible_moves = attack_moves

            # összevetés a hazard_moves listával

    return possible_moves


def hazard_remover(possible_moves: List[str], hazard_moves: List[str]) -> List[str]:
    # összevetés a hazard_moves listával
    safe = []
    if len(hazard_moves) > 0:
        for move in possible_moves:
            if move not in hazard_moves:
                safe.append(move)

    # de ha a metszet üres kivonluk az esetleges ellentétes irányt
    if len(safe) > 0:
        possible_moves = safe

    return possible_moves


# megvizsgalja hogy van -e mellette vagy keresztben mellette testresz
def has_body_neighbour(board: BoardData, x: int, y: int) -> bool:
    for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1],
                   [x + 1, y + 1], [x + 1, y - 1], [x - 1, y + 1], [x - 1, y - 1]]:
        if 0 <= i < board.width and 0 <= j < board.height:
            if board.board[j][i].name in ["head", "body", "tail"]:
                return True

    return False


def death_recursion(data: Dict, board: BoardData, been: List[List], x: int, y: int):
    # fal
    if x < 0 or y < 0 or x >= board.width or y >= board.height:
        return
    # itt már jártunk
    if been[y][x] == 1:
        return
    # testrészből nem megyünk tovább
    if board.board[y][x].name in ["head", "body", "tail"]:
        return

    been[y][x] = 1

    for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
        if 0 <= i < board.width and 0 <= j < board.height:
            if has_body_neighbour(board, i, j):
                death_recursion(data, board, been, i, j)
            """
            for key in board.board[y][x].arrive_time:
                if key == data["you"]["id"]:
                    if board.board[y][x].arrive_time[key] + 1 >= board.board[j][i].dis_time:
                        death_recursion(data, board, been, i, j)
            """


# lehetséges útvonalak rekurzív bejárása, önmagadba fordulás ellen
def avoid_death(data: Dict, board: BoardData, possible_moves: List[str]) -> List[str]:
    tx = data["you"]["body"][len(data["you"]["body"]) - 1]["x"]
    ty = data["you"]["body"][len(data["you"]["body"]) - 1]["y"]
    been = [[0 for x in range(board.width)] for y in range(board.height)]

    for [i, j] in [[tx + 1, ty], [tx - 1, ty], [tx, ty + 1], [tx, ty - 1]]:
        death_recursion(data, board, been, i, j)

    hx = data["you"]["head"]["x"]
    hy = data["you"]["head"]["y"]
    states = []

    if board.board[ty][tx].dis_time == 1 and data["you"]["length"] > 3:
        been[ty][tx] = 1

    for [i, j, direction] in [[hx + 1, hy, "right"], [hx - 1, hy, "left"], [hx, hy + 1, "up"], [hx, hy - 1, "down"]]:
        if 0 <= i < board.width and 0 <= j < board.height:
            if been[j][i] == 1:
                states.append(["safe", direction])
            else:
                states.append(["deadly", direction])
        else:
            states.append(["deadly", direction])

    if "safe" in [states[0][0], states[1][0], states[2][0], states[3][0]]:
        for state in states:
            if state[0] == "deadly":
                if state[1] in possible_moves:
                    possible_moves.remove(state[1])

    return possible_moves


# támadás


# két pont közötti legrövidebb útvonal??
def shortest_way():
    pass


def choose_move(data: Dict, board: BoardData) -> str:
    possible_moves = ["up", "down", "left", "right"]
    hazard_moves = []

    possible_moves = avoid_obstacles(data, board, possible_moves, hazard_moves)
    print(f"{data['turn']}. turn, moves of avoid_obstacles: {possible_moves}")

    possible_moves = avoid_death(data, board, possible_moves)
    print(f"{data['turn']}. turn, moves of avoid_death: {possible_moves}")

    possible_moves = who_to_head(data, board, possible_moves)
    print(f"{data['turn']}. turn, moves of who_to_head: {possible_moves}")

    possible_moves = hazard_remover(possible_moves, hazard_moves)
    print(f"{data['turn']}. turn, moves of hazard_remover: {possible_moves}")

    possible_moves = find_food_better(data, board, possible_moves)
    print(f"{data['turn']}. turn, moves of find_food_better: {possible_moves}")

    """
    if data["you"]["health"] < data["you"]["length"] + 2:
        possible_moves = find_food(data, board, possible_moves)
        print(f"{data['turn']}. turn, moves of find_food: {possible_moves}")
    else:
        possible_moves = avoid_food(data, board, possible_moves)
        print(f"{data['turn']}. turn, moves of avoid_food: {possible_moves}")

    
    moves = [ ["right",   "right",  "right",  "right",  "right",  "right",  "up"],
              ["down",    "down",   "up",     "left",   "up",     "left",   "up"], \
              ["down",    "down",   "up",     "down",   "up",     "down",   "up"], \
              ["right",   "down",   "up",     "down",   "up",     "down",   "up"], \
              ["down",    "left",   "up",     "down",   "up",     "down",   "up"], \
              ["right",   "down",   "up",     "down",   "up",     "down",   "up"], \
              ["down",    "left",   "left",   "down",   "left",   "down",   "left"]]

    if data["you"]["head"]["y"] == 2 and data["you"]["head"]["x"] == 1 and data["you"]["length"] == 45:
      moves[2][1] = "left"
    if data["you"]["head"]["y"] == 0 and data["you"]["head"]["x"] == 1 and data["you"]["length"] == 49:
      moves[0][1] = "up"

    x = data["you"]["head"]["x"]
    y = data["you"]["head"]["y"]

    move = moves[y][x]
    """

    # támadás ha hosszú és nem éhes vagyok, egyébként kajakeresés

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    if len(possible_moves) != 0:
        move = random.choice(possible_moves)
    else:
        move = ""

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
