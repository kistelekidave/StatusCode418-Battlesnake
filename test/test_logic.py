import unittest
from src.board_data import BoardData
from src.item_type import ItemType
from src.logic import Logic


class TestLogic(unittest.TestCase):

    def setUp(self):
        self.game_state = {
            "height": 5,
            "width": 5,
            "food": [],
            "hazards": [],
            "snakes": [
                {}
            ]
        }
        self.board_data = BoardData(self.game_state, "standard")

    def test_help_avoid_snake_body(self):
        cell = self.board_data.board[2][2]
        cell.type = ItemType.BODY
        dead_moves, hazard_moves = [], []
        Logic._help_avoid_snake(self.board_data, dead_moves, hazard_moves, 2, 2, "up")
        self.assertIn("up", dead_moves)

    def test_help_avoid_snake_tail_eaten(self):
        cell = self.board_data.board[2][2]
        cell.type = ItemType.TAIL
        cell.health = 100
        dead_moves, hazard_moves = [], []
        Logic._help_avoid_snake(self.board_data, dead_moves, hazard_moves, 2, 2, "up")
        self.assertIn("up", dead_moves)

    def test_help_avoid_snake_hazard(self):
        cell = self.board_data.board[2][2]
        cell.type = ItemType.HAZARD
        dead_moves, hazard_moves = [], []
        Logic._help_avoid_snake(self.board_data, dead_moves, hazard_moves, 2, 2, "right")
        self.assertIn("right", hazard_moves)

    def test_has_body_neighbour(self):
        self.board_data.board[2][3].type = ItemType.BODY
        data = {"game": {"ruleset": {"name": "standard"}}}
        result = Logic._has_body_neighbour(data, self.board_data, 2, 2)
        self.assertTrue(result)

    def test_has_body_neighbour_wrapped(self):
        wrapped_board = BoardData(self.game_state, "wrapped")
        wrapped_board.board[4][0].type = ItemType.BODY
        data = {"game": {"ruleset": {"name": "wrapped"}}}
        result = Logic._has_body_neighbour(data, wrapped_board, 0, 0)
        self.assertTrue(result)

    def test_avoid_obstacles_with_body(self):
        self.board_data.board[2][3].type = ItemType.BODY
        data = {"you": {"head": {"x": 2, "y": 2}}, "game": {"ruleset": {"name": "standard"}}}
        possible_moves = ["up", "down", "left", "right"]
        hazard_moves = []
        result = Logic._avoid_obstacles(data, self.board_data, possible_moves, hazard_moves)
        self.assertNotIn("right", result)

    def test_avoid_obstacles_walls(self):
        data = {"you": {"head": {"x": 0, "y": 0}}, "game": {"ruleset": {"name": "standard"}}}
        possible_moves = ["up", "down", "left", "right"]
        hazard_moves = []
        result = Logic._avoid_obstacles(data, self.board_data, possible_moves, hazard_moves)
        self.assertNotIn("left", result)
        self.assertNotIn("down", result)

    def test_hazard_remover(self):
        possible_moves = ["up", "down", "left"]
        hazard_moves = ["left"]
        result = Logic._hazard_remover(possible_moves, hazard_moves)
        self.assertNotIn("left", result)

    def test_hazard_remover_all_hazard(self):
        possible_moves = ["up"]
        hazard_moves = ["up"]
        result = Logic._hazard_remover(possible_moves, hazard_moves)
        self.assertEqual(result, ["up"])


if __name__ == '__main__':
    unittest.main()
