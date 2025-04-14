from src.item_type import ItemType
from src.utility import Utility


class ArriveTimeCalculator:

    # DFS graph traversal
    # TODO: BFS might be better
    @staticmethod
    def arrive_time_calculator(x: int, y: int, id: str, board_data, number: int):
        for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
            if board_data.modename == "wrapped":  # wrapped change
                i, j = Utility.wrapped_coords(i, j, board_data.width, board_data.height)
            if 0 <= i < board_data.width and 0 <= j < board_data.height:
                if board_data.board[j][i].type in [ItemType.CLEAR, ItemType.FOOD, ItemType.HAZARD]:
                    if id not in board_data.board[j][i].arrive_time or board_data.board[j][i].arrive_time[id] > number:
                        board_data.board[j][i].arrive_time[id] = number
                        ArriveTimeCalculator.arrive_time_calculator(i, j, id, board_data, number + 1)

    @staticmethod
    def calculate_for_all_snakes(board_data, snakes: list[dict]):
        # arrive_time megállapítása minden snakenek
        for snake in snakes:
            ArriveTimeCalculator.arrive_time_calculator(snake["head"]["x"], snake["head"]["y"], snake["id"], board_data, 1)