from CurrencyRouletteGame import CurrencyRouletteGame
from MemoryGame import MemoryGame
from GuessGame import GuessGame
from flask import Flask, render_template, request

app = Flask(__name__)


# welcomes the player
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        name = request.form['name']
        name = name.capitalize()
        welcome_message = f"Hello {name} and welcome to the World of Games (WoG).\n" \
                          "Here you can find many cool games to play."
        return render_template('welcome.html', message=welcome_message)
    else:
        return render_template('welcome.html')


# loads the games menu to select a game and difficulty, returns game and difficulty as a chained string
@app.route('/menu', methods=['GET', 'POST'])
def load_game():
    request.method = 'GET '
    games_list = {"1": MemoryGame, "2": GuessGame, "3": CurrencyRouletteGame}

    game_played = request.form.get('game', None)
    game_difficulty = request.form.get('difficulty', None)

    menu = ('''Please choose a game to play:
            1.Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back
            2.Guess Game - guess a number and see if you chose like the computer
            3.Currency Roulette - try and guess the value of a random amount of USD in ILS
            Enter 0 to exit''')

    if not game_played is None and (game_played.isdigit() and 1 <= int(game_played) <= 3):
        if not game_difficulty is None and (game_difficulty.isdigit() and 1 <= int(game_played) <= 5):
            game_picked = games_list[game_played](game_difficulty)
            is_lost = game_picked.play()
            if is_lost:
                return render_template('main.html', message="you lost!")
            else:
                return render_template('main.html', message="you won!")

        else:
            difficulty_message = "Please choose game difficulty from 1 (easy) to 5 (hard)"
            return render_template('main.html', message=menu, difficulty=difficulty_message)
    elif game_played == "0":
        return render_template('main.html', message='Goodbye!')
    else:
        return render_template('main.html', message=menu)
