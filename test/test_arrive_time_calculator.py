import unittest
from src.board_data import BoardData
from src.arrive_time_calculator import ArriveTimeCalculator


class TestArriveTimeCalculator(unittest.TestCase):

    def setUp(self):
        self.game_state = {
            "height": 5,
            "width": 5,
            "food": [{"x": 1, "y": 1}, {"x": 3, "y": 3}],
            "hazards": [{"x": 1, "y": 0}],
            "snakes": [
                {
                    "id": "snake1",
                    "name": "Sneky McSnek Face",
                    "health": 54,
                    "body": [
                        {"x": 1, "y": 3},
                        {"x": 1, "y": 3},
                        {"x": 0, "y": 2}
                    ],
                    "latency": "123",
                    "head": {"x": 1, "y": 3},
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
                        {"x": 3, "y": 2},
                        {"x": 3, "y": 1},
                        {"x": 3, "y": 0}
                    ],
                    "latency": "123",
                    "head": {"x": 3, "y": 2},
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
        self.board_data = BoardData(self.game_state, modename="standard")
        self.board_data.refresh(self.game_state)

    def test_arrival_times_set_correctly(self):
        head_x, head_y = 2, 2
        ArriveTimeCalculator.calculate_for_all_snakes(self.board_data, self.game_state["snakes"])
        
        self.assertIn("snake1", self.board_data.board[3][3].arrive_time)
        self.assertEqual(self.board_data.board[3][3].arrive_time["snake1"], 2)

    def test_arrival_does_not_pass_through_body(self):
        ArriveTimeCalculator.calculate_for_all_snakes(self.board_data, self.game_state["snakes"])
        for segment in self.game_state["snakes"][0]["body"]:
            x, y = segment["x"], segment["y"]
            self.assertNotIn("snake1", self.board_data.board[y][x].arrive_time)

    def test_arrival_respects_wrapping_mode(self):
        self.board_data.modename = "wrapped"
        self.game_state["snakes"][0]["head"] = {"x": 0, "y": 0}
        self.game_state["snakes"][0]["body"] = [
            {"x": 0, "y": 0},
            {"x": 0, "y": 1},
            {"x": 0, "y": 2},
        ]
        self.board_data.refresh(self.game_state)

        ArriveTimeCalculator.calculate_for_all_snakes(self.board_data, self.game_state["snakes"])

        wrapped_coords = [(4, 0), (0, 4)]
        for x, y in wrapped_coords:
            with self.subTest(x=x, y=y):
                self.assertIn("snake1", self.board_data.board[y][x].arrive_time)
                self.assertEqual(self.board_data.board[y][x].arrive_time["snake1"], 1)


if __name__ == '__main__':
    unittest.main()
