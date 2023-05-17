from Utils import SCORES_FILE_NAME
from os import listdir


# add game score after winning to scores file
def add_score(difficulty):
    # check if score file exists, else starts from 0
    if SCORES_FILE_NAME in listdir():
        file = open(SCORES_FILE_NAME)
        score = file.read()
        score = int(score)
        file.close()
    else:
        score = 0
    # calculate new score
    score += 5 + 3 * int(difficulty)
    # write new score to score file
    file = open(SCORES_FILE_NAME, 'w')
    file.write(str(score))
    file.close()