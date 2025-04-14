import unittest
from src.utility import Utility

class TestUtility(unittest.TestCase):
    def test_manhattan_distance(self):
        self.assertEqual(Utility.distance({"x": 0, "y": 0}, {"x": 3, "y": 4}), 7)
        self.assertEqual(Utility.distance({"x": 2, "y": 1}, {"x": 2, "y": 1}), 0)

    def test_wrapped_coords(self):
        self.assertEqual(Utility.wrapped_coords(2, 3, 5, 5), (2, 3))
        self.assertEqual(Utility.wrapped_coords(2, 5, 5, 5), (2, 0))
        self.assertEqual(Utility.wrapped_coords(2, 5, 5, 5), (2, 0))

    # see board coordinates decription in README
    def test_get_direction(self):
        self.assertEqual(Utility.get_direction(1, 1, 0, 1), "down")
        self.assertEqual(Utility.get_direction(1, 1, 2, 1), "up")
        self.assertEqual(Utility.get_direction(1, 1, 1, 0), "left")
        self.assertEqual(Utility.get_direction(1, 1, 1, 2), "right")

if __name__ == '__main__':
    unittest.main()