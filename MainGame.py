from Live import load_game, welcome, app

# Start the Flask app
if __name__ == '__main__':
    app.run()

# prints a welcome messege
welcome()

# prints games menu, returns game and difficulty as a chained string
load_game()
