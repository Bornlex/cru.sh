from src import state
from src import fruits
from src import display


if __name__ == '__main__':
    columns = [
        state.Column(4, rand_init=True),
        state.Column(4, rand_init=True),
        state.Column(4, rand_init=True),
    ]
    console = display.Console()
    print("Cru.sh")
    print("  Swap: col1, row1, col2, row2")

    gs = state.GameState(columns, console)
    gs.loop()

    while True:
        action = input("> ")
        
        if action == "exit":
            break

        tokens = action.split()
        if len(tokens) != 4:
            print("4 numbers needed.")
            continue
        
        try:
            for token in tokens:
                token = int(token)
        except:
            print("Only numbers.")
            continue

        col1, row1, col2, row2 = int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])
        gs.swap((col1, row1), (col2, row2))
        gs.loop()
