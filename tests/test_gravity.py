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
        a = fruits.Apple()
        b = fruits.Banana()
        k = fruits.Kiwi()
        s = [a, b, k]
        column = state.Column(size=s)
        column.gravity()
        self.assertTrue(column.full)
        self.assertEquals(a, column[0])
        self.assertEquals(b, column[1])
        self.assertEquals(k, column[2])

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
            self.assertTrue(isinstance(column[i], fruits.Fruit))
    
