import copy
import random
from typing import Union

from src import fruits
from src import display


class RandomGenerator:
    __allowed_fruits = [fruits.GreenApple, fruits.RedApple, fruits.Kiwi, fruits.Pineapple]
    __block = fruits.Block
    __empty = fruits.Empty
    
    @staticmethod
    def fruits_list(n: int):
        return random.choices(RandomGenerator.__allowed_fruits, k=n)

    @staticmethod
    def get_fruit():
        return random.choice(RandomGenerator.__allowed_fruits)


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
        for i in range(len(state1)):
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

    def __setitem__(self, index, item):
        assert 0 <= index < len(self.__state)
        self.__state[index] = item

    def __len__(self):
        return len(self.__state)

    def __gravity_iter(self):
        """
        Applies one iteration of gravity.
        """
        for i in range(len(self.__state)):
            index = len(self.__state) - i - 1
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
            if self.compare_states(self.__state, previous_state):
                # gravity alone cannot fill the whole column, probably an empty cell is located below a rock
                return 1
            if isinstance(self.__state[0], fruits.Empty):
                self.__state[0] = RandomGenerator.get_fruit()()
                
        return 0


class GameState:
    def __init__(self, columns: list[Column], console: display.Console):
        self.__columns = columns
        self.__console = console

    def __getitem__(self, index: int):
        assert 0 <= index < len(self.__columns)
        return self.__columns[index]

    def __len__(self):
        return len(self.__columns)

    def __search_for_adjacent_fruits(
            self, position: tuple[int, int],
            k: int = 3,
            state: list[Column] = None
    ) -> list[tuple[int, int]]:
        """
        Searches for adjacent fruits that should be destroyed or transformed into a super fruit.

        :param position: the position of the first fruit of the combination
        :param k: the minimum number of adjacent fruits to look for
        :param state: the state to look into (in case it is not the self state)
        :return: the list of adjacent positions
        """
        col, row = position
        results = []

        state = state if state is not None else self

        found = []
        # search in line
        for c in range(col, len(state)):
            if isinstance(state[c][row], type(state[col][row])):
                found.append((c, row))
            else:
                break

        if len(found) >= k:
            results += found

        found = []
        # search in column
        for r in range(row, len(state[col])):
            if isinstance(state[col][r], type(state[col][row])):
                found.append((col, r))
            else:
                break

        if len(found) >= k:
            results += found

        return results

    @staticmethod
    def compare_states(state1, state2):
        assert len(state1) == len(state2)
        for i in range(len(state1)):
            assert len(state1[i]) == len(state2[i])
            for j in range(len(state1[i])):
                if type(state1[i][j]) != type(state2[i][j]):
                    return False
        return True

    def swap(self, position1: tuple[int, int], position2: tuple[int, int]):
        """
        Swaps two adjacent fruits.

        @position1: the position of the first fruit
        @position2: the position of the second fruit
        @return: None, just update the game state
        """
        col1, row1 = position1
        col2, row2 = position2

        # Make sure we are inside the grid
        assert 0 <= col1 < len(self)
        assert 0 <= col2 < len(self)
        assert 0 <= row1 < len(self[col1])
        assert 0 <= row2 < len(self[col2])
        # Make sure the fruits are adjacent
        assert (
            (col1 == col2 and (row1 == row2 - 1 or row1 == row2 + 1)) or
            (row1 == row2 and (col1 == col2 - 1 or col1 == col2 + 1))
        )

        # copy state and perform swap inside it to check if it connects fruits
        virtual_state = copy.deepcopy(self.__columns)
        tmp = virtual_state[col2][row2]
        virtual_state[col2][row2] = virtual_state[col1][row1]
        virtual_state[col1][row1] = tmp

        virtual_found1 = self.__search_for_adjacent_fruits((col1, 0), state=virtual_state)
        virtual_found2 = self.__search_for_adjacent_fruits((0, row1), state=virtual_state)
        virtual_found3 = self.__search_for_adjacent_fruits((col2, 0), state=virtual_state)
        virtual_found4 = self.__search_for_adjacent_fruits((0, row2), state=virtual_state)
        virtual_found = virtual_found1 + virtual_found2 + virtual_found3 + virtual_found4
        if len(virtual_found) == 0:
            # the swap does not connect any fruit, so we do not perform it
            return

        # the proposed swap indeed connects fruits, so we perform it on the real state
        tmp = self[col2][row2]
        self[col2][row2] = self[col1][row1]
        self[col1][row1] = tmp

    def destroy(self):
        """
        Destroy similar aligned candies (at least 3).

        TODO: pop super fruits in case of special patterns
        """
        to_set_empty = []
        for col in range(len(self)):
            for row in range(len(self[col])):
                adjacent_fruits = self.__search_for_adjacent_fruits((col, row))
                to_set_empty += adjacent_fruits

        for col, row in to_set_empty:
            self[col][row] = fruits.Empty()

    def gravity(self):
        """
        Applies gravity on the game state.
        """
        for i in range(len(self)):
            self[i].gravity()

    def loop(self):
        while True:
            self.__console.display_game_state(self)
            previous_state = copy.deepcopy(self.__columns)
            self.gravity()
            self.destroy()
            if self.compare_states(previous_state, self.__columns):
                break
