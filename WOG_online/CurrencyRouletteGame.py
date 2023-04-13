from py_currency_converter import convert

def get_money_interval(difficulty, usd_amount: int):
    money_interval = [None] * 3

    # converting USD to ILS for given amount

    money_interval[0] = convert(base="USD", amount=usd_amount, to=["ILS"])["ILS"]

    # getting interval min/max as follows:
    # for given difficulty d, and total value of money t the interval is: (t - (5 - d), t +(5 - d))
    money_interval[1] = money_interval[0] - (5 - int(difficulty))
    money_interval[2] = money_interval[0] + (5 - int(difficulty))
    return money_interval