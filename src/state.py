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

    @property
    def columns(self):
        return self.__columns

    @staticmethod
    def __search_for_adjacent_fruits(
            position: tuple[int, int],
            state: list[Column],
            k: int = 3,
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

    def __check_for_possible_combinations(self, state: list[Column]) -> bool:
        """
        In order to know if there exists a potential combination, we will use the so called "bruteforce" method.
        Try to swap every adjacent fruits and check for combination. As simple as that, but very ugly.

        @state: the state to look into
        @return: True if there is a potential combination, False otherwise
        """
        for col in range(len(state) - 1):
            for row in range(len(state[col]) - 1):
                swapped_state = self.__swap((col, row), (col, row + 1), state)
                adjacent_fruits = self.__search_for_adjacent_fruits((col, row), state=swapped_state)
                if len(adjacent_fruits) > 0:
                    return True

                swapped_state = self.__swap((col, row), (col + 1, row), state)
                adjacent_fruits = self.__search_for_adjacent_fruits((col, row), state=swapped_state)
                if len(adjacent_fruits) > 0:
                    return True

        return False

    @staticmethod
    def compare_states(state1, state2):
        assert len(state1) == len(state2)
        for i in range(len(state1)):
            assert len(state1[i]) == len(state2[i])
            for j in range(len(state1[i])):
                if type(state1[i][j]) != type(state2[i][j]):
                    return False
        return True

    @staticmethod
    def __swap(position1: tuple[int, int], position2: tuple[int, int], game_state: list[Column]):
        col1, row1 = position1
        col2, row2 = position2

        state = copy.deepcopy(game_state)

        # Make sure we are inside the grid
        assert 0 <= col1 < len(state)
        assert 0 <= col2 < len(state)
        assert 0 <= row1 < len(state[col1])
        assert 0 <= row2 < len(state[col2])
        # Make sure the fruits are adjacent
        assert (
            (col1 == col2 and (row1 == row2 - 1 or row1 == row2 + 1)) or
            (row1 == row2 and (col1 == col2 - 1 or col1 == col2 + 1))
        )

        virtual_state = copy.deepcopy(state)
        tmp = virtual_state[col2][row2]
        virtual_state[col2][row2] = virtual_state[col1][row1]
        virtual_state[col1][row1] = tmp

        found1 = GameState.__search_for_adjacent_fruits((col1, 0), state=virtual_state)
        found2 = GameState.__search_for_adjacent_fruits((0, row1), state=virtual_state)
        found3 = GameState.__search_for_adjacent_fruits((col2, 0), state=virtual_state)
        found4 = GameState.__search_for_adjacent_fruits((0, row2), state=virtual_state)
        found = found1 + found2 + found3 + found4
        if len(found) == 0:
            return

        tmp = state[col2][row2]
        state[col2][row2] = state[col1][row1]
        state[col1][row1] = tmp

        return state

    def swap(self, position1: tuple[int, int], position2: tuple[int, int]):
        """
        Swaps two adjacent fruits.

        @position1: the position of the first fruit
        @position2: the position of the second fruit
        @state: the state to swap into in case it is not the current self
        @return: None, just update the game state
        """
        columns = self.__swap(position1, position2, self.__columns)
        if columns is not None:
            self.__columns = columns

    def destroy(self):
        """
        Destroy similar aligned candies (at least 3).

        TODO: pop super fruits in case of special patterns
        """
        to_set_empty = []
        for col in range(len(self)):
            for row in range(len(self[col])):
                adjacent_fruits = self.__search_for_adjacent_fruits((col, row), state=self.__columns)
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
