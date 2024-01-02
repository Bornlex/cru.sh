import unittest

from src import state
from src import fruits
from src import display


class TestSearch(unittest.TestCase):
    def test_search_adjacent_same_row(self):
        c1 = state.Column(size=[
            fruits.RedApple(), fruits.Kiwi(), fruits.GreenApple()
        ])
        c2 = state.Column(size=[
            fruits.RedApple(), fruits.GreenApple(), fruits.Kiwi()
        ])
        c3 = state.Column(size=[
            fruits.RedApple(), fruits.Kiwi(), fruits.GreenApple()
        ])
        gs = state.GameState([c1, c2, c3], console=display.Console())
        position = (0, 0)
        found = gs._GameState__search_for_adjacent_fruits(position, state=gs.columns)
        self.assertEqual(3, len(found))
        self.assertTrue(isinstance(found[0], tuple))

    def test_search_adjacent_same_row2(self):
        c1 = state.Column(size=[
            fruits.RedApple(), fruits.Kiwi(), fruits.GreenApple()
        ])
        c2 = state.Column(size=[
            fruits.RedApple(), fruits.GreenApple(), fruits.Kiwi()
        ])
        c3 = state.Column(size=[
            fruits.RedApple(), fruits.Kiwi(), fruits.GreenApple()
        ])
        c4 = state.Column(size=[
            fruits.RedApple(), fruits.GreenApple(), fruits.Kiwi()
        ])
        gs = state.GameState([c1, c2, c3, c4], console=display.Console())
        position = (0, 0)
        found = gs._GameState__search_for_adjacent_fruits(position, state=gs.columns)
        self.assertEqual(4, len(found))

    def test_search_adjacent_same_column(self):
        c1 = state.Column(size=[
            fruits.RedApple(), fruits.Kiwi(), fruits.GreenApple()
        ])
        c2 = state.Column(size=[
            fruits.RedApple(), fruits.RedApple(), fruits.RedApple()
        ])
        c3 = state.Column(size=[
            fruits.Kiwi(), fruits.Kiwi(), fruits.GreenApple()
        ])
        gs = state.GameState([c1, c2, c3], console=display.Console())
        position = (1, 0)
        found = gs._GameState__search_for_adjacent_fruits(position, state=gs.columns)
        self.assertEqual(3, len(found))

    def test_search_adjacent_empty(self):
        c1 = state.Column(size=[
            fruits.RedApple(), fruits.Kiwi(), fruits.GreenApple()
        ])
        c2 = state.Column(size=[
            fruits.RedApple(), fruits.RedApple(), fruits.RedApple()
        ])
        c3 = state.Column(size=[
            fruits.Kiwi(), fruits.Kiwi(), fruits.GreenApple()
        ])
        gs = state.GameState([c1, c2, c3], console=display.Console())
        position = (0, 0)
        found = gs._GameState__search_for_adjacent_fruits(position, state=gs.columns)
        self.assertEqual(0, len(found))
