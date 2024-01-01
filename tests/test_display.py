import sys
import unittest

from src import fruits


class DisplayFruit(unittest.TestCase):
    def test_print_fruits(self):
        fs = [
            fruits.RedApple(),
            fruits.Banana(),
            fruits.Blueberry(),
            fruits.Kiwi()
        ]
        print([f.icon for f in fs])
