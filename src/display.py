import sys

from src import fruits


class Console:
    _separator = "--------\n"

    @staticmethod
    def __fetch_game_state(gs):
        max_size = -1
        for i in range(len(gs)):
            if len(gs[i]) > max_size:
                max_size = len(gs[i])

        lines = [[fruits.Empty() for _ in range(len(gs))] for _ in range(max_size)]

        for col in range(len(gs)):
            for i in range(min(max_size, len(gs[col]))):
                lines[i][col] = gs[col][i].icon

        return lines

    def display_game_state(self, gs):
        lines = self.__fetch_game_state(gs)
        content = self._separator
        for line in lines:
            content += " ".join(line) + "\n"
        content += self._separator
        
        sys.stdout.write("\r")
        sys.stdout.flush()
        sys.stdout.write(content)
        sys.stdout.flush()
