from typing import Tuple


class Utility:

    @staticmethod
    def distance(point1: dict, point2: dict) -> int:
        return abs(point1["x"] - point2["x"]) + abs(point1["y"] - point2["y"])

    @staticmethod
    def wrapped_coords(x: int, y: int, width: int, height: int) -> Tuple[int, int]:
        return x % width, y % height

    @staticmethod
    def get_direction(y, x, last_y, last_x) -> str:
        if last_x > x:
            return "right"
        elif last_x < x:
            return "left"
        elif last_y > y:
            return "up"
        else:
            return "down"
