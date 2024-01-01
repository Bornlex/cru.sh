import copy
import random
from typing import Union

from src import fruits



class RandomGenerator:
    @staticmethod
    def fruits_list(n: int):
        choices = fruits.Fruit.__subclasses__()
        return random.choices(choices, k=n)


class Column:
    def __init__(self, size: Union[int|list], rand_init: bool = False):
        if isinstance(size, int):
            if rand_init:
                self.__state = [c() for c in RandomGenerator.fruits_list(size)]
            else:
                self.__state = [fruits.Empty()] * size
        else:
            self.__state = size

    @staticmethod
    def compare_states(state1: list, state2: list):
        assert len(state1) == len(state2)
        for i in range(state1):
            if state1[i] != state2[i]:
                return False
        return True

    @property
    def empty(self):
        for fruit in self.__state:
            if isinstance(fruit, fruits.Fruit):
                return False
        return True

    @property
    def full(self):
        for fruit in self.__state:
            if isinstance(fruit, fruits.Empty):
                return False
        return True

    def __getitem__(self, index):
        assert 0 <= index < len(self.__state)
        return self.__state[index]

    def __len__(self):
        return len(self.__state)

    def __gravity_iter(self):
        """
        Applies one iteration of gravity.
        """
        for i in range(len(self.__state)):
            index = len(self.__state - i - 1)
            if isinstance(self.__state[index], fruits.Empty):
                if index <= 0 or isinstance(self.__state[index - 1], fruits.Block):
                    continue
                tmp = self.__state[index]
                self.__state[index] = self.__state[index - 1]
                self.__state[index - 1] = tmp

    def gravity(self):
        """
        Applies the full gravity process.
        @return: 0 if it does not need fruits from neighbors columns, 1 if it does.
        """
        while not self.full:
            previous_state = copy.deepcopy(self.__state)
            self.__gravity_iter()
            if self.compare_state(self.__state, previous_state):
                # gravity alone cannot fill the whole column, probably an empty cell is located below a rock
                return 1
        return 0


class GameState:
    def __init__(self, columns: list[Column]):
        self.__columns = columns

    def __getitem__(self, index):
        assert 0 <= index < len(self.__columns)
        return self.__columns[index]

    def __len__(self):
        return len(self.__columns)

    def swap(self):
        """
        Swaps two adjacent fruits.
        """
        pass

    def destroy(self):
        """
        Destroy similar aligned candies (at least 3).
        """
        pass

    def gravity(self):
        """
        Applies gravity on the game state.
        """
        pass
