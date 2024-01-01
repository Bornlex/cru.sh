import unittest

from src import state
from src import fruits



class TestGravity(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_gravity_column_full(self):
        """
        Test the gravity mechanism with a full column.
        Nothing should change.
        """
        a = fruits.RedApple()
        b = fruits.Banana()
        k = fruits.Kiwi()
        s = [a, b, k]
        column = state.Column(size=s)
        column.gravity()
        self.assertTrue(column.full)
        self.assertEqual(a, column[0])
        self.assertEqual(b, column[1])
        self.assertEqual(k, column[2])

    def test_gravity_column_empty(self):
        """
        Test the gravity mechanism with an empty column.
        It should be filled with fruits.
        """
        size = 4
        column = state.Column(size=size)
        column.gravity()
        self.assertTrue(column.full)
        for i in range(size):
            self.assertTrue(column[i], fruits.Fruit)

    def test_gravity_last_missing(self):
        a = fruits.RedApple()
        b = fruits.Banana()
        k = fruits.Kiwi()
        s = [a, b, k, fruits.Empty()]
        column = state.Column(size=s)
        column.gravity()
        self.assertTrue(isinstance(column[0], fruits.Fruit))
        self.assertEqual(column[1], a)
        self.assertEqual(column[2], b)
        self.assertEqual(column[3], k)
        
