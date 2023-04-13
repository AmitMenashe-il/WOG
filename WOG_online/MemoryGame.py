from random import randint

def generate_sequence(difficulty):
    numbers_list = [None] * int(difficulty)
    for i in range(int(difficulty)):
        numbers_list[i] = str(randint(1, 101))
    return numbers_list


def is_list_equal(difficulty, generated_number_list, user_number_list):
    list_equal = True
    generated_number_list.sort()
    user_number_list.sort()
    for number in range(int(difficulty)):
        if not user_number_list[number] == generated_number_list[number] and list_equal:
            list_equal = False
    return list_equal