from py_currency_converter import convert
from random import randint
from flask import Flask, render_template, request

class CurrencyRouletteGame:

    def __init__(self, difficulty):
        self.difficulty = difficulty

    # get the current currency rate from USD to ILS and generates an interval:
    def get_money_interval(self, usd_amount: int):
        money_interval = [None] * 2

        # converting USD to ILS for given amount

        total_usd_in_ils = convert(base="USD", amount=usd_amount, to=["ILS"])["ILS"]

        # getting interval min/max as follows:
        # for given difficulty d, and total value of money t the interval is: (t - (5 - d), t +(5 - d))
        print(f"the real value was {total_usd_in_ils}")
        money_interval[0] = total_usd_in_ils - (5 - int(self.difficulty))
        money_interval[1] = total_usd_in_ils + (5 - int(self.difficulty))
        print(f"the acceptable interval to win was: {money_interval}")
        return money_interval

    # prompts the user to enter a guess of value to a given amount of USD
    def get_guess_from_user(self, usd_amount):
        currency_guess = ""
        split_guess = ""

        while not ((len(split_guess) == 2 and currency_guess[0].isdigit() and currency_guess[1].isdigit()) or (
                len(split_guess) == 1 and currency_guess.isdigit())):
            currency_guess = input(f"please enter your guess for current currency value of {usd_amount} USD in ILS\n")
            split_guess = currency_guess.split(".")

        return currency_guess

    # play the game. Will return True / False if the user lost or won.
    def play(self):
        usd_amount = randint(1, 100)
        currency_guess = self.get_guess_from_user(usd_amount)
        money_interval = self.get_money_interval(usd_amount)
        return not money_interval[0] <= float(currency_guess) <= money_interval[1]
