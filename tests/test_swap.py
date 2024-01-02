import unittest

from src import state
from src import fruits
from src import display


class SwapTest(unittest.TestCase):
    def setUp(self):
        """
        Constructs the following state:
        🍎🥝🍎
        🥝🍎🍌
        🍏🍌🥝
        🥝🍌🥝
        """
        columns = [
            state.Column(size=[fruits.RedApple(), fruits.Kiwi(), fruits.GreenApple(), fruits.Kiwi()]),
            state.Column(size=[fruits.Kiwi(), fruits.RedApple(), fruits.Banana(), fruits.Banana()]),
            state.Column(size=[fruits.RedApple(), fruits.Banana(), fruits.Kiwi(), fruits.Kiwi()]),
        ]
        self.gs = state.GameState(columns, display.Console())
    
    def test_simple_swap(self):
        position1 = (1, 0)
        position2 = (1, 1)
        candy1 = self.gs[position1[0]][position1[1]]
        candy2 = self.gs[position2[0]][position2[1]]
        
        self.gs.swap(position1, position2)

        candy1_swaped = self.gs[position1[0]][position1[1]]
        candy2_swaped = self.gs[position2[0]][position2[1]]

        self.assertEqual(candy1, candy2_swaped)
        self.assertEqual(candy2, candy1_swaped)

    def test_simple_swap_not_adjacent(self):
        position1 = (0, 1)
        position2 = (0, 0)
        candy1 = self.gs[position1[0]][position1[1]]
        candy2 = self.gs[position2[0]][position2[1]]

        self.gs.swap(position1, position2)

        candy1_swaped = self.gs[position1[0]][position1[1]]
        candy2_swaped = self.gs[position2[0]][position2[1]]

        self.assertEqual(candy1, candy1_swaped)
        self.assertEqual(candy2, candy2_swaped)

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
