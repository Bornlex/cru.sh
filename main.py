from src import state
from src import fruits
from src import display


if __name__ == '__main__':
    columns = [
        state.Column(4, rand_init=True),
        state.Column(4, rand_init=True),
        state.Column(4, rand_init=True),
    ]
    gs = state.GameState(columns)
    console = display.Console()
    console.display_game_state(gs)
