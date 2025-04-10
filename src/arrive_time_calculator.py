from board_data import BoardData
from utility import Utility


class ArriveTimeCalculator:

    # DFS graph traversal
    # TODO: BFS might be better
    @staticmethod
    def arrive_time_calculator(x: int, y: int, id: str, board_data: BoardData, number: int):
        for [i, j] in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
            if board_data.modename == "wrapped":  # wrapped change
                i, j = Utility.wrapped_coords(i, j)
            if 0 <= i < board_data.width and 0 <= j < board_data.height:
                if board_data.board[j][i].type in ["clear", "food", "hazard"]:
                    if id not in board_data.board[j][i].arrive_time or board_data.board[j][i].arrive_time[id] > number:
                        board_data.board[j][i].arrive_time[id] = number
                        ArriveTimeCalculator.arrive_time_calculator(i, j, id, number + 1)