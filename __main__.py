
from sherlock_game import GameManager, DEFAULT_CARDS

GAME_TRACKER = GameManager(DEFAULT_CARDS)

# Run a terminal to collect data.
inp = ""
while True:
    inp = input(">>> ")
    if inp[:4].upper() == 'QUIT':
        break
    else:
        GAME_TRACKER.run_q(inp)