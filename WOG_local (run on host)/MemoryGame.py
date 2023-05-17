from random import randint
from time import sleep


class MemoryGame:

    # sets the game difficulty as a property
    def __init__(self, difficulty):
        self.difficulty = difficulty

    # generates a list of random numbers between 1 to 101. The list length is difficulty.
    def generate_sequence(self):
        numbers_list = [None] * int(self.difficulty)
        for i in range(int(self.difficulty)):
            numbers_list[i] = str(randint(1, 101))
        return numbers_list

    # returns a list of numbers prompted from the user. The list length is in the size of difficulty.
    def get_list_from_user(self):
        numbers_list = [None] * int(self.difficulty)
        i = 0
        while i < (int(self.difficulty)):
            numbers_list[i] = input(
                f"Enter a number between 1 and 101, you need to enter {int(self.difficulty) - i} more numbers:\n")
            if not (numbers_list[i].isdigit() and 1 <= int(numbers_list[i]) <= 101):
                print("invalid input, try again")
                i -= 1
            i += 1

        return numbers_list

    # compares two lists, if they are equal The function returns True / False.
    def is_list_equal(self, generated_number_list, user_number_list):
        list_equal = True
        generated_number_list.sort()
        user_number_list.sort()
        for number in range(int(self.difficulty)):
            if not user_number_list[number] == generated_number_list[number]:
                list_equal = False
        return list_equal

    # play the game. returns True / False if the user lost or won.
    def play(self):

        generated_number_list = self.generate_sequence()
        print(generated_number_list, end="")
        sleep(0.7)
        print("", end="\r")

        user_number_list = self.get_list_from_user()
        print(f"the numbers were: {generated_number_list}")
        return not self.is_list_equal(generated_number_list, user_number_list)
