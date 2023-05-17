import os

SCORES_FILE_NAME ="Scores.txt"
BAD_RETURN_CODE = "666"

#clears the terminal screen
def screen_cleaner():
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')
