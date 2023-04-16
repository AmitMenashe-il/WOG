from random import randint


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
    def get_guess_from_user(self):
        user_guess = "-1"
        while not (user_guess.isdigit() and 1 <= int(user_guess) <= int(self.difficulty)):
            user_guess = input(f"please enter your guess, a number between 1 and {self.difficulty}:\n")
        return user_guess

    # compares the secret generated number to the user input
    def compare_results(self, user_guess: str):
        return self.secret_number == user_guess

    # play the game. returns True / False if the user lost or won
    def play(self):
        user_guess = self.get_guess_from_user()
        print(f"the number drawn was :{self.secret_number}")
        return not self.compare_results(user_guess)
