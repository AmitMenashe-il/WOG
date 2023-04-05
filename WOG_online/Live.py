#from CurrencyRouletteGame import CurrencyRouletteGame

from time import sleep
from random import randint

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'ranD0m_V3ry-5ecUre-seCreT_K3y'

@app.route('/MemoryGame/<int:difficulty>', methods=['GET', 'POST'])
def MemoryGame(difficulty):
    def generate_sequence(difficulty):
        numbers_list = [None] * int(difficulty)
        for i in range(int(difficulty)):
            numbers_list[i] = str(randint(1, 101))
        return numbers_list


    if "numbers_shown" not in session:
        game = "MemoryGame"
        generated_number_list = generate_sequence(difficulty)
        session['user_guess_length'] = int(difficulty)
        session['guess_list'] = [None] * session['user_guess_length']
        session['numbers_shown'] = True
        return render_template('memorygame_show.html', game=game, message=generated_number_list, difficulty=difficulty)


    while session['user_guess_length'] >0:

        user_guess = request.form.get('user_input', 'a')

        if user_guess.isdigit() and 1 <= int(user_guess) <= 101:
            session['guess_list'][user_guess_length-1] = int(user_guess)
            session['user_guess_length']-=1

        game_message = f"Enter a number between 1 and 101, you need to enter {session['user_guess_length']} more numbers:\n"
        if session['user_guess_length']>0:
            return render_template('game.html', game=game, message_request=game_message, difficulty=difficulty)
        else:
            break

    game_response=f"the numbers were: {generated_number_list}"
    del session['user_guess_length']
    del session['guess_list']
    del session['numbers_shown']
    #check if lists equal and get outcome


    return render_template('game.html',game=game, message_response=game_response)
@app.route('/GuessGame/<int:difficulty>', methods=['GET', 'POST'])
def GuessGame(difficulty):

    if 'secret_number' not in locals():
        game="GuessGame"
        secret_number = randint(1, int(difficulty))
        game_message = f"please enter your guess, a number between 1 and {difficulty}:"

    user_guess = request.form.get('user_input','a')

    if user_guess.isdigit() and (1 <= int(user_guess) <= int(difficulty)):
        random_number_msg = (f"the number drawn was : {secret_number}")
        session['outcome'] = user_guess == str(secret_number)
        return render_template('game.html',game=game, message_response=random_number_msg)
    else:
        return render_template('game.html',game=game, message_request=game_message,difficulty=difficulty)

@app.route('/CurrencyRouletteGame/<int:difficulty>', methods=['GET', 'POST'])
def CurrencyRouletteGame(difficulty):
    pass

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
def menu():
    games_list = {"1": "MemoryGame", "2": "GuessGame", "3": "CurrencyRouletteGame"}

    game_played = request.form.get('game')
    game_difficulty = request.form.get('difficulty')

    menu = ('''Please choose a game to play:
            1.Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back
            2.Guess Game - guess a number and see if you chose like the computer
            3.Currency Roulette - try and guess the value of a random amount of USD in ILS
            Enter 0 to exit''')

    #check game_played is valid, store it in session variable
    if not game_played is None and (game_played.isdigit() and 1 <= int(game_played) <= 3):
        session['game_played'] = game_played

    #if game chosen, check difficulty is valid
    if session.get('game_played'):
        if not game_difficulty is None and (game_difficulty.isdigit() and 1 <= int(game_difficulty) <= 5):
            game_played=games_list[session['game_played']]
            del session['game_played']
            return render_template('GameSelect.html',game_played=game_played,difficulty=game_difficulty)

        else:
            difficulty_message = "Please choose game difficulty from 1 (easy) to 5 (hard)"
            return render_template('menu.html', message=menu, difficulty=difficulty_message)
    elif game_played == "0":
        return render_template('menu.html', message='Goodbye!')
    else:
        return render_template('menu.html', message=menu)



@app.route('/outcome',methods=['GET', 'POST'])
def outcome():
            outcome = session['outcome']
            if not outcome:
                return render_template('endgame.html', message="you lost!")
            else:
                del session['outcome']
                return render_template('endgame.html', message="you won!")





# Start the Flask app
if __name__ == '__main__':
    app.run()

