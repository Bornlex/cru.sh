import unittest

from src import state


class SwapTest(unittest.TestCase):
    def setUp(self):
        columns = [
            state.Column(4, rand_init=True),
            state.Column(4, rand_init=True),
            state.Column(4, rand_init=True),
        ]
        self.gs = state.GameState(columns)
    
    def test_simple_swap(self):
        position1 = (0, 1)
        position2 = (0, 0)
        candy1 = self.gs[position1[0]][position1[1]]
        candy2 = self.gs[position2[0]][position2[1]]
        
        self.gs.swap(position1, position2)

        candy1_swaped = self.gs[position1[0]][position1[1]]
        candy2_swaped = self.gs[position2[0]][position2[1]]

        self.assertEqual(candy1, candy2_swaped)
        self.assertEqual(candy2, candy1_swaped)

    def test_out_of_bounds(self):
        position1 = (0, 0)
        position2 = (-1, 0)
        with self.assertRaises(AssertionError):
            self.gs.swap(position1, position2)

    def test_not_adjacent(self):
        position1 = (0, 1)
        position2 = (2, 0)
        with self.assertRaises(AssertionError):
            self.gs.swap(position1, position2)
