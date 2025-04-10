import random
from typing import List, Dict
from board_data import BoardData
from utility import Utility


class Logic:

    # iranyok kivalogatasa avoid_obstacles fuggveny szamara
    @staticmethod
    def _help_avoid_snake(board_data: BoardData, dead_moves: List[str], hazard_moves: List[str], x: int, y: int, direction: str):
        if board_data.board[y][x].type in ["head", "body"]:
            dead_moves.append(direction)

        elif board_data.board[y][x].type == "tail":
            if board_data.board[y][x].health == 100:
                dead_moves.append(direction)

        elif board_data.board[y][x].type == "hazard":
            hazard_moves.append(direction)

    # megvizsgalja hogy van -e mellette vagy keresztben mellette testresz
    @staticmethod
    def _has_body_neighbour(data: Dict, board_data: BoardData, x: int, y: int) -> bool:
        for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1],
                    [x + 1, y + 1], [x + 1, y - 1], [x - 1, y + 1], [x - 1, y - 1]]:
            if 0 <= i < board_data.width and 0 <= j < board_data.height:
                if board_data.board[j][i].type in ["head", "body", "tail"]:
                    return True

            elif data["game"]["ruleset"]["name"] == "wrapped":  # wrapped change
                i, j = Utility.wrapped_coords(i, j, board_data.width, board_data.height)
                if board_data.board[j][i].type in ["head", "body", "tail"]:
                    return True
        return False

    # wrapped modban vizsgaljon tovabb, ha kimenne a palyarol, atjon a tuloldalt
    @staticmethod
    def _death_recursion(data: Dict, board_data: BoardData, been: List[List], x: int, y: int):
        # wrappedben kulso koordinata atkerul a tuloldalra
        if data["game"]["ruleset"]["name"] == "wrapped":  # wrapped change
            x, y = Utility.wrapped_coords(i, j, board_data.width, board_data.height)

        # fal
        elif x < 0 or y < 0 or x >= board_data.width or y >= board_data.height:
            return

        # itt már jártunk
        if been[y][x] == 1:
            return
        # testrészből nem megyünk tovább
        if board_data.board[y][x].type in ["head", "body", "tail"]:
            return

        been[y][x] = 1

        for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
            if 0 <= i < board_data.width and 0 <= j < board_data.height:
                if Logic._has_body_neighbour(data, board_data, i, j):
                    Logic._death_recursion(data, board_data, been, i, j)
            elif data["game"]["ruleset"]["name"] == "wrapped":  # wrapped change
                i, j = Utility.wrapped_coords(i, j, board_data.width, board_data.height)
                if Logic._has_body_neighbour(data, board_data, i, j):
                    Logic._death_recursion(data, board_data, been, i, j)

    # who_to_head helper
    @staticmethod
    def _help_to_head(data: Dict, board_data: BoardData, x: int, y: int) -> list:
        can_go = True
        attack = False

        for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
            if data["game"]["ruleset"]["name"] == "wrapped":  # wrapped change
                i, j = Utility.wrapped_coords(i, j, board_data.width, board_data.height)
            if 0 <= i < board_data.width and 0 <= j < board_data.height:
                if board_data.board[j][i].type == "head":
                    if board_data.board[j][i].id != data["you"]["id"]:
                        if board_data.board[j][i].length >= data["you"]["length"]:
                            can_go = False
                        elif board_data.board[j][i].type != "hazard":
                            attack = True
        return [can_go, attack]

    # wrapped modban nem lehet falnak menni
    # pimitiv akadáaly kerules
    @staticmethod
    def _avoid_obstacles(data: dict, board_data: BoardData, possible_moves: List[str], hazard_moves: List[str]) -> List[str]:
        x = data["you"]["head"]["x"]
        y = data["you"]["head"]["y"]

        # da walls
        if data['game']['ruleset']['name'] != 'wrapped':
            if x == board_data.width - 1:
                possible_moves.remove("right")
            elif x == 0:
                possible_moves.remove("left")

            if y == board_data.height - 1:
                possible_moves.remove("up")
            elif y == 0:
                possible_moves.remove("down")

        # bodies and hazards
        dead_moves = []
        for [i, j, direction] in [[x + 1, y, "right"], [x - 1, y, "left"], [x, y + 1, "up"], [x, y - 1, "down"]]:
            if data["game"]["ruleset"]["name"] == "wrapped":  # wrapped change
                i, j = Utility.wrapped_coords(i, j, board_data.width, board_data.height)
            if 0 <= i < board_data.width and 0 <= j < board_data.height:
                Logic._help_avoid_snake(board_data, dead_moves, hazard_moves, i, j, direction)

        for move in dead_moves:
            if len(possible_moves) > 1:
                if move in possible_moves:
                    possible_moves.remove(move)
        return possible_moves

    # wrapped
    @staticmethod
    def _food_recursion(data: Dict, board_data: BoardData, been: List[List[int]], x: int, y: int, my_id: str):
        for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
            if data["game"]["ruleset"]["name"] == "wrapped":  # wrapped change
                i, j = Utility.wrapped_coords(i, j, board_data.width, board_data.height)
            if 0 <= i < board_data.width and 0 <= j < board_data.height:
                if board_data.board[j][i].type in ["clear", "hazard", "food"]:
                    if board_data.board[j][i].arrive_time[my_id] < board_data.board[y][x].arrive_time[my_id]:
                        if [j, i] not in been:
                            been.append([i, j])
                            Logic._food_recursion(data, board_data, been, i, j, my_id)

    # okosabb kajakereses erkezesi ido alapjan, utvonaltervezessel
    @staticmethod
    def _find_food_better(data: Dict, board_data: BoardData, possible_moves: List[str]) -> List[str]:
        fx = -1
        fy = -1
        im_first = False
        # closest_to_enemy = True
        my_time = Utility.distance({"x": 0, "y": 0}, {"x": board_data.width, "y": board_data.height})

        hx = data["you"]["head"]["x"]
        hy = data["you"]["head"]["y"]

        for food in data["board"]["food"]:
            temp_my_time = -1
            temp_im_first = True
            # saját időm
            if data["you"]["id"] in board_data.board[food["y"]][food["x"]].arrive_time:
                temp_my_time = board_data.board[food["y"]][food["x"]].arrive_time[data["you"]["id"]]

            # egyátalán eljutok -e oda
            if temp_my_time != -1:
                # mások hamarabb érnek -e oda
                for key in board_data.board[food["y"]][food["x"]].arrive_time:
                    if key != data["you"]["id"]:
                        if board_data.board[food["y"]][food["x"]].arrive_time[key] <= temp_my_time:
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
            # csak akkor jutunk el oda, ha benne van a mi arrive_time-unk
            if data["you"]["id"] in board_data.board[fy][fx].arrive_time:
                Logic._food_recursion(data, board_data, been, fx, fy, data["you"]["id"])

        food_moves = []
        # iranyok szelektalasa
        for [i, j, direction] in [[hx + 1, hy, "right"], [hx - 1, hy, "left"], [hx, hy + 1, "up"], [hx, hy - 1, "down"]]:
            if [i, j] in been and direction in possible_moves:
                food_moves.append(direction)

        if len(food_moves) > 0:
            possible_moves = food_moves

        return possible_moves

    # fejeles tervezes szomszedos mezokon
    # oda nem mehetsz ahova másik head el tud menni és nagyobb vagy egyenlő hosszú, CSAK HA MUSZÁLY
    # oda mész ahova másik head tud menni és rövidebb
    @staticmethod
    def _who_to_head(data: Dict, board_data: BoardData, possible_moves: List[str]) -> List[str]:
        x = data["you"]["head"]["x"]
        y = data["you"]["head"]["y"]
        attack_moves = []
        if len(possible_moves) > 1:

            for [i, j, direction] in [[x + 1, y, "right"], [x - 1, y, "left"], [x, y + 1, "up"], [x, y - 1, "down"]]:
                if data["game"]["ruleset"]["name"] == "wrapped":  # wrapped change
                    i, j = Utility.wrapped_coords(i, j, board_data.width, board_data.height)
                if 0 <= i < board_data.width and 0 <= j < board_data.height:
                    if board_data.board[j][i].type in ["clear", "food", "hazard"] or board_data.board[j][i].type == "tail" and board_data.board[j][i].dis_time == 1:
                        output = Logic._help_to_head(data, board_data, i, j)
                        if not output[0]:
                            if direction in possible_moves:
                                possible_moves.remove(direction)
                        elif output[1]:
                            if direction in possible_moves:
                                attack_moves.append(direction)

            if len(attack_moves) > 0:
                possible_moves = attack_moves
        return possible_moves

    @staticmethod
    def _hazard_remover(possible_moves: List[str], hazard_moves: List[str]) -> List[str]:
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

    # lehetséges útvonalak rekurzív bejárása, önmagadba fordulás ellen
    @staticmethod
    def _avoid_death(data: Dict, board_data: BoardData, possible_moves: List[str]) -> List[str]:
        tx = data["you"]["body"][len(data["you"]["body"]) - 1]["x"]
        ty = data["you"]["body"][len(data["you"]["body"]) - 1]["y"]
        been = [[0 for x in range(board_data.width)] for y in range(board_data.height)]

        for [i, j] in [[tx + 1, ty], [tx - 1, ty], [tx, ty + 1], [tx, ty - 1]]:
            Logic._death_recursion(data, board_data, been, i, j)

        hx = data["you"]["head"]["x"]
        hy = data["you"]["head"]["y"]
        states = []

        if board_data.board[ty][tx].dis_time == 1 and data["you"]["length"] > 3:
            been[ty][tx] = 1

        for [i, j, direction] in [[hx + 1, hy, "right"], [hx - 1, hy, "left"], [hx, hy + 1, "up"], [hx, hy - 1, "down"]]:
            if 0 <= i < board_data.width and 0 <= j < board_data.height:
                if been[j][i] == 1:
                    states.append(["safe", direction])
                else:
                    states.append(["deadly", direction])
            elif data["game"]["ruleset"]["name"] == "wrapped":  # wrapped change
                i, j = Utility.wrapped_coords(i, j, board_data.width, board_data.height)
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

    @staticmethod
    def choose_move(data: Dict, board_data: BoardData) -> str:
        possible_moves = ["up", "down", "left", "right"]
        hazard_moves = []

        possible_moves = Logic._avoid_obstacles(data, board_data, possible_moves, hazard_moves)
        print(f"{data['turn']}. turn, moves of avoid_obstacles: {possible_moves}")

        possible_moves = Logic._avoid_death(data, board_data, possible_moves)
        print(f"{data['turn']}. turn, moves of avoid_death: {possible_moves}")

        possible_moves = Logic._who_to_head(data, board_data, possible_moves)
        print(f"{data['turn']}. turn, moves of who_to_head: {possible_moves}")

        possible_moves = Logic._hazard_remover(possible_moves, hazard_moves)
        print(f"{data['turn']}. turn, moves of hazard_remover: {possible_moves}")

        possible_moves = Logic._find_food_better(data, board_data, possible_moves)
        print(f"{data['turn']}. turn, moves of find_food_better: {possible_moves}")

        # támadás ha hosszú és nem éhes vagyok, egyébként kajakeresés

        # Choose a random direction from the remaining possible_moves to move in, and then return that move
        if len(possible_moves) != 0:
            move = random.choice(possible_moves)
        else:
            move = ""

        print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")
        print(f"wrapped: {data['game']['ruleset']['name'] == 'wrapped'}")
        return move
