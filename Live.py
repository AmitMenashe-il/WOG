from CurrencyRouletteGame import CurrencyRouletteGame
from MemoryGame import MemoryGame
from GuessGame import GuessGame
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'ranD0m_V3ry-5ecUre-seCreT_K3y'

# welcomes the player
@app.route('/', methods=['GET', 'POST'])
def welcome():

    if request.method == 'POST':
        name = request.form.get('name')
        name = name.capitalize()
        welcome_message = f"Hello {name} and welcome to the World of Games (WoG).\n" \
                          "Here you can find many cool games to play."
        return render_template('welcome.html', message=welcome_message)
    else:
        return render_template('welcome.html')


# loads the games menu to select a game and difficulty, returns game and difficulty as a chained string
@app.route('/menu', methods=['GET', 'POST'])
def load_game():

    games_list = {"1": MemoryGame, "2": GuessGame, "3": CurrencyRouletteGame}

    game_played = request.form.get('game')
    game_difficulty = request.form.get('difficulty')

    menu = ('''Please choose a game to play:
            1.Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back
            2.Guess Game - guess a number and see if you chose like the computer
            3.Currency Roulette - try and guess the value of a random amount of USD in ILS
            Enter 0 to exit''')

    if not game_played is None and (game_played.isdigit() and 1 <= int(game_played) <= 3) :
        session['game_played']=game_played

    if session.get('game_played'):
        if not game_difficulty is None and (game_difficulty.isdigit() and 1 <= int(game_difficulty) <= 5):
            game_played=session['game_played']
            game_picked = games_list[game_played](game_difficulty)
            game_picked.play()
            session['game_played'] = None
            outcome=session['outcome']
            if outcome:
                return render_template('endgame.html', message="you lost!")
            else:
                return render_template('endgame.html', message="you won!")
            session['outcome']=None

        else:
            difficulty_message = "Please choose game difficulty from 1 (easy) to 5 (hard)"
            return render_template('menu.html', message=menu, difficulty=difficulty_message)
    elif game_played == "0":
        return render_template('menu.html', message='Goodbye!')
    else:
        return render_template('menu.html', message=menu)
