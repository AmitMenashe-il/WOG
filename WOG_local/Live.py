from CurrencyRouletteGame import CurrencyRouletteGame
from MemoryGame import MemoryGame
from GuessGame import GuessGame


# welcomes the player
def welcome(name):
    # case first letter-
    name = name.capitalize()
    print(f"Hello {name} and welcome to the World of Games (WoG).\n" \
          "Here you can find many cool games to play.")


# loads the games menu to select a game and difficulty, returns game and difficulty as a chained string
def load_game():
    games_list = {"1": MemoryGame, "2": GuessGame, "3": CurrencyRouletteGame}
    game_played = ""

    # while not choose quit
    while not game_played == "0":

        # clear previous game selection
        game_played = ""

        # print menu
        while not (game_played.isdigit() and 1 <= int(game_played) <= 3):
            print('''Please choose a game to play:
            1.Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back
            2.Guess Game - guess a number and see if you chose like the computer
            3.Currency Roulette - try and guess the value of a random amount of USD in ILS
            Enter 0 to exit''')
            game_played = input()

            # quit if pick 0
            if game_played == "0":
                break

        # quit if pick 0
        if game_played == "0":
            break

        # clear previous difficulty selection
        game_difficulty = ""

        # pick difficulty
        while not (game_difficulty.isdigit() and 1 <= int(game_difficulty) <= 5):
            game_difficulty = input("Please choose game difficulty from 1 (easy) to 5 (hard):\n")

        # play picked game
        game_picked = games_list[game_played](game_difficulty)
        is_lost = game_picked.play()
        if is_lost:
            print("you lost!")
        else:
            print("you won!")
