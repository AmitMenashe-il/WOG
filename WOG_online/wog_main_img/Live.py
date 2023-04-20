#games modules
from MemoryGame import generate_sequence, is_list_equal
from CurrencyRouletteGame import get_money_interval
from GuessGame import generate_number, compare_results
from Score import add_score
from random import randint
#mysql modules
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import sessionmaker, declarative_base
from alembic.config import Config
from alembic import command
from os import environ
#flask modules
from flask import Flask, render_template, request, session

#init flask and secret key for session variables
app = Flask(__name__)
app.secret_key = 'ranD0m_V3ry-5ecUre-seCreT_K3y'


@app.route('/MemoryGame/<int:difficulty>', methods=['GET', 'POST'])
def MemoryGame(difficulty):
    # on first run init variables and show the numbers
    if "generated_number_list" not in session:
        session['generated_number_list'] = generate_sequence(difficulty)
        session['user_guess_length'] = int(difficulty)
        session['guess_list'] = [None] * session['user_guess_length']
        return render_template('memorygame_show.html', game=session['game_played'],
                               message=session['generated_number_list'], difficulty=difficulty)

    # get user guess
    while session['user_guess_length'] > 0:

        user_guess = request.form.get('user_input', 'a')
        # validate guess is legal
        if user_guess.isdigit() and 1 <= int(user_guess) <= 101:
            session['guess_list'][session['user_guess_length'] - 1] = user_guess
            session['user_guess_length'] -= 1

        game_message = f"Enter a number between 1 and 101, you need to enter {session['user_guess_length']} more numbers:\n"
        if session['user_guess_length'] > 0:
            return render_template('game.html', game=session['game_played'], message_request=game_message,
                                   difficulty=difficulty)
        else:
            break
    # show numbers drawn, set outcome and delete game variables
    game_response = f"the numbers were: {session['generated_number_list']}"
    session['outcome'] = is_list_equal(difficulty, session['generated_number_list'], session['guess_list'])
    del session['generated_number_list']
    del session['user_guess_length']
    del session['guess_list']
    # check if lists equal and get outcome

    return render_template('game.html', game=session['game_played'], message_response=game_response)


@app.route('/GuessGame/<int:difficulty>', methods=['GET', 'POST'])
def GuessGame(difficulty):
    if 'secret_number' not in locals():
        secret_number = generate_number(difficulty)
        game_message = f"please enter your guess, a number between 1 and {difficulty}:"

    user_guess = request.form.get('user_input', 'a')

    if user_guess.isdigit() and (1 <= int(user_guess) <= int(difficulty)):
        random_number_msg = (f"the number drawn was : {secret_number}")
        session['outcome'] = compare_results(user_guess, str(secret_number))
        return render_template('game.html', game=session['game_played'], message_response=random_number_msg)
    else:
        return render_template('game.html', game=session['game_played'], message_request=game_message,
                               difficulty=difficulty)


@app.route('/CurrencyRouletteGame/<int:difficulty>', methods=['GET', 'POST'])
def CurrencyRouletteGame(difficulty):

    #initilaze usd amount and messages
    if 'usd_amount' not in session:
        session['usd_amount'] = randint(1, 100)
        game_message = f"please enter your guess for current currency value of {session['usd_amount']} USD in ILS:"
        session['money_interval']=get_money_interval(difficulty,session['usd_amount'])

    user_guess = request.form.get('user_input', 'a')
    split_guess = user_guess.split(".")

    if ((len(split_guess) == 2 and user_guess[0].isdigit() and user_guess[1].isdigit()) or (len(split_guess) == 1 and user_guess.isdigit())):
        message_response = (f"the real value was {session['money_interval'][0]}, the acceptable interval to win was: {session['money_interval'][1]},{session['money_interval'][2]}")

        session['outcome'] = session['money_interval'][1] <= float(user_guess) <= session['money_interval'][2]
        del session['usd_amount']
        del session['money_interval']
        return render_template('game.html', game=session['game_played'], message_response=message_response)
    else:
        return render_template('game.html', game=session['game_played'], message_request=game_message,difficulty=difficulty)

@app.route('/Scores', methods=['GET', 'POST'])
def score_server():

    # Alembic configuration file path (none, env.py in folder)
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location",
                                "/app")
    command.upgrade(alembic_cfg, "head")

    # Initialize database engine
    engine = create_engine(f"mysql://{environ['USER_NAME']}:{environ['USER_PASSWORD']}@DB/{environ['DB_NAME']}?host=DB")

    # Declare database table
    class user_scores_table(declarative_base()):
        __tablename__ = environ['TABLE_NAME']
        id = Column(Integer, primary_key=True)
        username = Column(String)
        score = Column(Integer)
        timestamp = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if the value exists in the database, and update it or create it if it doesn't
    scores = session.query(user_scores_table).all()
    return render_template('score.html', scores=scores)

# welcomes the player
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        name = request.form.get('name')
        session['name'] = name.capitalize()
        welcome_message = f"Hello {session['name']} and welcome to the World of Games (WoG).\n" \
                          "Here you can find many cool games to play."
        session['score']=0
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

    # check game_played is valid, store it in session variable
    if not game_played is None and (game_played.isdigit() and 1 <= int(game_played) <= 3):
        session['game_played'] = game_played

    # if game chosen, check difficulty is valid
    if 'game_played' in session:
        if not game_difficulty is None and (game_difficulty.isdigit() and 1 <= int(game_difficulty) <= 5):
            session['difficulty'] = game_difficulty
            if session['game_played'].isdigit():
                session['game_played'] = games_list[session['game_played']]
                return render_template('GameSelect.html', game_played=session['game_played'], difficulty=game_difficulty)
            else:
                return render_template('GameSelect.html', game_played=session['game_played'], difficulty=game_difficulty)


        else:
            difficulty_message = "Please choose game difficulty from 1 (easy) to 5 (hard)"
            return render_template('menu.html', message=menu, difficulty=difficulty_message)
    elif game_played == "0":
        del session['name']
        del session['score']
        return render_template('menu.html', message='Goodbye!')
    else:
        return render_template('menu.html', message=menu)


@app.route('/outcome', methods=['GET', 'POST'])
def outcome():
    del session['game_played']
    if not session['outcome']:
        del session['outcome']
        del session['difficulty']
        return render_template('endgame.html', message="you lost!")
    else:
        del session['outcome']
        session['score'] += 5 + 3 * int(session['difficulty'])
        add_score(session['name'],session['score'])
        del session['difficulty']
        return render_template('endgame.html', message="you won!")


# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
