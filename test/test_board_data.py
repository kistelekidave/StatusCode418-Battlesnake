import unittest
from src.board_data import BoardData
from src.item_type import ItemType


class TestBoardData(unittest.TestCase):

    def setUp(self):
        self.game_state = {
            "height": 5,
            "width": 5,
            "food": [{"x": 3, "y": 3}],
            "hazards": [{"x": 4, "y": 4}],
            "snakes": [
                {
                    "id": "snake1",
                    "name": "Sneky McSnek Face",
                    "health": 54,
                    "body": [
                        {"x": 0, "y": 0},
                        {"x": 1, "y": 0},
                        {"x": 2, "y": 0}
                    ],
                    "latency": "123",
                    "head": {"x": 0, "y": 0},
                    "length": 3,
                    "shout": "why are we shouting??",
                    "squad": "1",
                    "customizations":{
                        "color":"#26CF04",
                        "head":"smile",
                        "tail":"bolt"
                    }
                },
                {
                    "id": "snake2",
                    "name": "Snake Guy",
                    "health": 34,
                    "body": [
                        {"x": 0, "y": 1},
                        {"x": 1, "y": 1},
                        {"x": 1, "y": 2}
                    ],
                    "latency": "123",
                    "head": {"x": 0, "y": 1},
                    "length": 3,
                    "shout": "aaaaa",
                    "squad": "1",
                    "customizations":{
                        "color":"#26CF04",
                        "head":"smile",
                        "tail":"bolt"
                    }
                }
            ]
        }
        self.board_data = BoardData(self.game_state, "standard")

    def test_initial_board(self):
        self.assertEqual(len(self.board_data.board), 5)
        self.assertEqual(len(self.board_data.board[0]), 5)

    def test_place_food(self):
        self.board_data.place_food(self.game_state["food"])
        self.assertEqual(self.board_data.board[3][3].type, ItemType.FOOD)

    def test_place_hazards(self):
        self.board_data.place_hazards(self.game_state["hazards"])
        self.assertEqual(self.board_data.board[4][4].type, ItemType.HAZARD)

    def test_place_snakes(self):
        self.board_data.place_snakes(self.game_state["snakes"])
        self.assertEqual(self.board_data.board[0][0].type, ItemType.HEAD)
        self.assertEqual(self.board_data.board[0][1].type, ItemType.BODY)
        self.assertEqual(self.board_data.board[0][2].type, ItemType.TAIL)

    def test_refresh(self):
        self.board_data.refresh(self.game_state)
        self.assertEqual(self.board_data.board[3][3].type, ItemType.FOOD)
        self.assertEqual(self.board_data.board[4][4].type, ItemType.HAZARD)
        self.assertEqual(self.board_data.board[0][0].type, ItemType.HEAD)


if __name__ == '__main__':
    unittest.main()
