from Live import load_game, welcome
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='/WOG')


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/', methods=['POST'])
def process_form():
    name = request.form['name']
    welcome(name)
    load_game()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
