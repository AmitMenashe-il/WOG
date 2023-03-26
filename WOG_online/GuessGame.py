from random import randint
from flask import Flask, render_template, request, session

app = Flask(__name__)


# welcomes the player
class GuessGame:

    # sets the secret number for the game and the difficulty as properties
    def __init__(self, difficulty: str):
        # generates a number between 1 to difficulty and save it to secret_number.
        def generate_number(difficulty: str):
            secret_number = randint(1, int(difficulty))
            return str(secret_number)

        self.difficulty = difficulty
        self.secret_number = generate_number(difficulty)

    # prompts the user for a number between 1 to difficulty and returns the number.
    @app.route('/game', methods=['GET', 'POST'])
    def get_guess_from_user(self):

        user_guess = request.form.get('user_input','a')

        game_message = f"please enter your guess, a number between 1 and {self.difficulty}:"

        if user_guess.isdigit() and (1 <= int(user_guess) <= int(self.difficulty)):
            session['user_guess']=user_guess
            return
        else:
            return render_template('game.html', message0=game_message,game_played=session['game_played'])


    # compares the secret generated number to the user input
    def compare_results(self, user_guess: str):
        return self.secret_number == user_guess

    # play the game. returns True / False if the user lost or won
    @app.route('/game', methods=['GET', 'POST'])
    def play(self):
        return self.get_guess_from_user()
        random_number = (f"the number drawn was :{self.secret_number}")
        session['outcome'] = self.compare_results(session['user_guess'])
        session['user_guess'] = None
        return render_template('game.html', message1=random_number)