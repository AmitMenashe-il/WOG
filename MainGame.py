from Live import load_game, welcome
from flask import Flask, render_template, request

#app = Flask(__name__, template_folder='/WOG')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/', methods=['POST'])
def process_form():
    name = request.form['name']
    welcome_message = welcome(name)
    return render_template('welcome.html', message=welcome_message)

@app.route('/play', methods=['POST'])
def play_game():
    menu='''Please choose a game to play:\n
            1.Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back\n
            2.Guess Game - guess a number and see if you chose like the computer\n
            3.Currency Roulette - try and guess the value of a random amount of USD in ILS\n
            Enter 0 to exit'''
    return render_template('main.html', message=menu)
    load_game()