from random import randint
def generate_number(difficulty: str):
    secret_number = randint(1, int(difficulty))
    return str(secret_number)
def compare_results(user_guess: str,secret_number: str):
    return secret_number == user_guess
